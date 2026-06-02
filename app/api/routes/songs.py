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
    db: Session = Depends(get_session),
) -> List[Song]:
    """List all songs."""
    repo = SongRepository(db)
    return repo.get_all(skip=skip, limit=limit)


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
