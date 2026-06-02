"""Tests for song versions, references, and download visibility."""
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.deps import get_session
from app.main import app
from app.models import DownloadLink, LinkVisibility, SongReference
from app.repositories import SongRepository


@pytest.fixture
def client(db: Session) -> Generator[TestClient, None, None]:
    """Create a TestClient using the in-memory database."""
    app.dependency_overrides[get_session] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_versions_include_base_and_order_stored_versions(
    client: TestClient,
    db: Session,
) -> None:
    """Stored versions are ordered with the base version first."""
    repo = SongRepository(db)
    song = repo.create(title="Rental", slug="rental")
    repo.add_version(song.id, "Studio Session", sort_order=20)
    repo.add_version(song.id, "Base Mix", is_base_version=True, sort_order=99)
    repo.add_version(song.id, "Early Demo", sort_order=10)

    response = client.get(f"/songs/{song.id}/versions")

    assert response.status_code == 200
    assert [version["title"] for version in response.json()] == [
        "Base Mix",
        "Early Demo",
        "Studio Session",
    ]
    assert response.json()[0]["is_base_version"] is True


def test_versions_include_virtual_base_for_existing_song(
    client: TestClient,
    db: Session,
) -> None:
    """Songs without stored versions still expose the base song version."""
    repo = SongRepository(db)
    song = repo.create(title="Cigarettes", slug="cigarettes")

    response = client.get(f"/songs/{song.id}/versions")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": None,
            "song_id": song.id,
            "title": "Cigarettes",
            "version_type": "current",
            "release_status": "unknown",
            "is_base_version": True,
            "recorded_date": None,
            "surfaced_date": None,
            "source_name": None,
            "source_url": None,
            "confidence": 1.0,
            "sort_order": 0,
            "notes": None,
        }
    ]


def test_references_are_not_download_links(
    client: TestClient,
    db: Session,
) -> None:
    """References are returned as metadata and never power download redirects."""
    repo = SongRepository(db)
    song = repo.create(title="GoPro", slug="gopro")
    db.add(
        SongReference(
            song_id=song.id,
            source_name="Session notes",
            source_url="https://example.com/session-notes",
            source_type="manual",
            description="notes",
        )
    )
    db.commit()

    references_response = client.get(f"/songs/{song.id}/references")
    download_response = client.get(f"/downloads/{song.id}", follow_redirects=False)

    assert references_response.status_code == 200
    assert references_response.json()[0]["source_name"] == "Session notes"
    assert download_response.status_code == 404


def test_downloads_use_public_links_only(
    client: TestClient,
    db: Session,
) -> None:
    """Download redirects only use public links, including link_id requests."""
    repo = SongRepository(db)
    song = repo.create(title="K Like A Russian", slug="k-like-a-russian")
    bot_link = DownloadLink(
        song_id=song.id,
        label="Bot only",
        url="https://example.com/bot-only",
        visibility=LinkVisibility.BOT.value,
    )
    public_link = DownloadLink(
        song_id=song.id,
        label="Public",
        url="https://example.com/public",
        visibility=LinkVisibility.PUBLIC.value,
    )
    db.add_all([bot_link, public_link])
    db.commit()
    db.refresh(bot_link)

    automatic_response = client.get(f"/downloads/{song.id}", follow_redirects=False)
    private_response = client.get(
        f"/downloads/{song.id}",
        params={"link_id": bot_link.id},
        follow_redirects=False,
    )

    assert automatic_response.status_code in {302, 307}
    assert automatic_response.headers["location"] == "https://example.com/public"
    assert private_response.status_code == 403
