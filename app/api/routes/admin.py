"""Admin routes."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_session
from app.core.auth import require_admin
from app.repositories import SongRepository
from app.services import SongService

router = APIRouter(prefix="/admin/songs", tags=["admin"])


class CreateSongRequest(BaseModel):
    """Create song request."""

    title: str
    era_name: Optional[str] = None
    release_status: str = "unknown"
    download_status: str = "metadata_only"
    official_url: Optional[str] = None
    api_download_url: Optional[str] = None
    notes: Optional[str] = None


class UpdateSongRequest(BaseModel):
    """Update song request."""

    title: Optional[str] = None
    release_status: Optional[str] = None
    download_status: Optional[str] = None
    official_url: Optional[str] = None
    api_download_url: Optional[str] = None
    notes: Optional[str] = None


@router.post("")
async def create_song(
    req: CreateSongRequest,
    db: Session = Depends(get_session),
    _: dict = Depends(require_admin),
) -> dict:
    """Create a new song."""
    service = SongService(db)
    song = service.create_song(
        title=req.title,
        era_name=req.era_name,
        release_status=req.release_status,
        download_status=req.download_status,
        official_url=req.official_url,
        api_download_url=req.api_download_url,
        notes=req.notes,
    )
    return {"id": song.id, "title": song.title}


@router.patch("/{song_id}")
async def update_song(
    song_id: int,
    req: UpdateSongRequest,
    db: Session = Depends(get_session),
    _: dict = Depends(require_admin),
) -> dict:
    """Update a song."""
    repo = SongRepository(db)
    update_data = req.dict(exclude_unset=True)
    song = repo.update(song_id, **update_data)

    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    return {"id": song.id, "title": song.title}


@router.delete("/{song_id}")
async def delete_song(
    song_id: int,
    db: Session = Depends(get_session),
    _: dict = Depends(require_admin),
) -> dict:
    """Delete a song."""
    repo = SongRepository(db)
    if not repo.delete(song_id):
        raise HTTPException(status_code=404, detail="Song not found")
    return {"deleted": True}
