"""Era routes."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_session
from app.models import Era, Song
from app.repositories import EraRepository, SongRepository

router = APIRouter(prefix="/eras", tags=["eras"])


class EraResponse(BaseModel):
    """Era response model."""

    id: int
    name: str
    years: Optional[str]
    description: Optional[str]

    class Config:
        """Pydantic config."""
        from_attributes = True


class SongResponse(BaseModel):
    """Song response model."""

    id: int
    title: str
    slug: str

    class Config:
        """Pydantic config."""
        from_attributes = True


@router.get("", response_model=list[EraResponse])
async def list_eras(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
) -> list[Era]:
    """List all eras."""
    repo = EraRepository(db)
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{era_id}", response_model=EraResponse)
async def get_era(
    era_id: int,
    db: Session = Depends(get_session),
) -> Era:
    """Get a specific era."""
    repo = EraRepository(db)
    era = repo.get_by_id(era_id)
    if not era:
        raise HTTPException(status_code=404, detail="Era not found")
    return era


@router.get("/{era_id}/songs", response_model=list[SongResponse])
async def get_era_songs(
    era_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
) -> list[Song]:
    """Get songs from an era."""
    era_repo = EraRepository(db)
    if not era_repo.get_by_id(era_id):
        raise HTTPException(status_code=404, detail="Era not found")

    song_repo = SongRepository(db)
    return song_repo.get_by_era_id(era_id, skip=skip, limit=limit)
