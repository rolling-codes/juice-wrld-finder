"""Song routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.api.deps import get_session
from app.repositories import SongRepository
from app.models import Song

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

    class Config:
        """Pydantic config."""
        from_attributes = True


@router.get("", response_model=List[SongResponse])
async def list_songs(
    skip: int = 0,
    limit: int = 100,
    era_id: int | None = None,
    release_status: str | None = None,
    producer_id: int | None = None,
    db: Session = Depends(get_session),
) -> List[Song]:
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

    return query.offset(skip).limit(limit).all()


@router.get("/{song_id}", response_model=SongResponse)
async def get_song(
    song_id: int,
    db: Session = Depends(get_session),
) -> Song:
    """Get a specific song."""
    repo = SongRepository(db)
    song = repo.get_by_id(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song
