"""Song routes."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_session
from app.core.security import redact_private_urls
from app.models import Song
from app.repositories import SongRepository

router = APIRouter(prefix="/songs", tags=["songs"])


class SongResponse(BaseModel):
    """Song response model."""

    id: int
    title: str
    slug: str
    release_status: str
    download_status: str
    official_url: Optional[str]
    notes: Optional[str]
    era_id: Optional[int]
    version_count: int = 0
    reference_count: int = 0
    source_names: list[str] = Field(default_factory=list)

    class Config:
        """Pydantic config."""
        from_attributes = True


class SongVersionResponse(BaseModel):
    """Song version response model."""

    id: Optional[int]
    song_id: int
    title: str
    version_type: str
    release_status: str
    is_base_version: bool
    recorded_date: Optional[str]
    surfaced_date: Optional[str]
    source_name: Optional[str]
    source_url: Optional[str]
    confidence: float
    sort_order: int
    notes: Optional[str]

    class Config:
        """Pydantic config."""
        from_attributes = True


class SongReferenceResponse(BaseModel):
    """Song reference response model."""

    id: int
    song_id: int
    source_type: str
    source_name: str
    source_url: Optional[str]
    description: Optional[str]
    confidence: float

    class Config:
        """Pydantic config."""
        from_attributes = True


@router.get("", response_model=list[SongResponse])
async def list_songs(
    skip: int = 0,
    limit: int = 100,
    era_id: int | None = None,
    release_status: str | None = None,
    producer_id: int | None = None,
    db: Session = Depends(get_session),
) -> list[SongResponse]:
    """List all songs with optional filters."""
    query = db.query(Song)

    if era_id:
        query = query.filter(Song.era_id == era_id)

    if release_status:
        query = query.filter(Song.release_status == release_status)

    if producer_id:
        query = query.filter(
            Song.producers.any(id=producer_id)
        )

    songs = query.offset(skip).limit(limit).all()
    return [_song_response(song) for song in songs]


@router.get("/{song_id}", response_model=SongResponse)
async def get_song(
    song_id: int,
    db: Session = Depends(get_session),
) -> SongResponse:
    """Get a specific song."""
    repo = SongRepository(db)
    song = repo.get_by_id(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return _song_response(song)


@router.get("/{song_id}/versions", response_model=list[SongVersionResponse])
async def get_song_versions(
    song_id: int,
    db: Session = Depends(get_session),
) -> list[SongVersionResponse]:
    """Get known versions for a song, including the base song version."""
    repo = SongRepository(db)
    song = repo.get_by_id(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    versions = repo.get_versions(song_id)
    if any(version.is_base_version for version in versions):
        return versions

    base_version = SongVersionResponse(
        id=None,
        song_id=song.id,
        title=song.title,
        version_type="current",
        release_status=song.release_status,
        is_base_version=True,
        recorded_date=None,
        surfaced_date=None,
        source_name=None,
        source_url=None,
        confidence=1.0,
        sort_order=0,
        notes=None,
    )
    return [base_version, *versions]


@router.get("/{song_id}/references", response_model=list[SongReferenceResponse])
async def get_song_references(
    song_id: int,
    db: Session = Depends(get_session),
) -> list[SongReferenceResponse]:
    """Get non-download references for a song."""
    repo = SongRepository(db)
    song = repo.get_by_id(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    references = repo.get_references(song_id)
    for reference in references:
        if reference.source_url:
            reference.source_url = redact_private_urls(reference.source_url)
    return references


def _song_response(song: Song) -> SongResponse:
    """Build a public song response with version/reference summary metadata."""
    source_names = sorted(
        {
            reference.source_name
            for reference in song.references
            if reference.source_name
        }
    )
    return SongResponse(
        id=song.id,
        title=song.title,
        slug=song.slug,
        release_status=song.release_status,
        download_status=song.download_status,
        official_url=song.official_url,
        notes=song.notes,
        era_id=song.era_id,
        version_count=len(song.versions),
        reference_count=len(song.references),
        source_names=source_names,
    )
