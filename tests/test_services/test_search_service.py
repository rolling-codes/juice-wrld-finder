"""Test search service."""
from sqlalchemy.orm import Session

from app.repositories import SongRepository
from app.services import SearchService


def test_search_exact_match(db: Session) -> None:
    """Test exact title search."""
    repo = SongRepository(db)
    song = repo.create(title="Lucid Dreams", slug="lucid-dreams")

    service = SearchService(db)
    results = service.search("lucid dreams")

    assert len(results) > 0
    assert results[0].song.id == song.id
    assert results[0].confidence == 100.0


def test_search_fuzzy_match(db: Session) -> None:
    """Test fuzzy matching with typos."""
    repo = SongRepository(db)
    repo.create(title="Lucid Dreams", slug="lucid-dreams")

    service = SearchService(db)
    results = service.search("lucid drams")  # Typo

    assert len(results) > 0
    assert results[0].song.title == "Lucid Dreams"


def test_search_by_alias(db: Session) -> None:
    """Test search by alias."""
    from app.models import Alias

    repo = SongRepository(db)
    song = repo.create(title="Lucid Dreams", slug="lucid-dreams")

    alias = Alias(song_id=song.id, alias="Lucid Dreamz")
    db.add(alias)
    db.commit()

    service = SearchService(db)
    results = service.search("lucid dreamz")

    assert len(results) > 0
    assert results[0].song.id == song.id


def test_search_no_results(db: Session) -> None:
    """Test search with no matches."""
    service = SearchService(db)
    results = service.search("nonexistent")

    assert len(results) == 0
