"""Download link management routes."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_session
from app.core.auth import require_admin
from app.core.security import redact_private_urls
from app.models import DownloadLink, LinkVisibility
from app.repositories import SongRepository

router = APIRouter(prefix="/links", tags=["links"])


class LinkResponse(BaseModel):
    """Download link response."""
    id: int
    song_id: int
    label: str
    url: str
    link_type: str
    visibility: str

    class Config:
        from_attributes = True


class CreateLinkRequest(BaseModel):
    """Create link request."""
    song_id: int
    label: str
    url: str
    link_type: str = "other"
    visibility: str = "bot"


class UpdateLinkRequest(BaseModel):
    """Update link request."""
    label: Optional[str] = None
    url: Optional[str] = None
    link_type: Optional[str] = None
    visibility: Optional[str] = None


@router.get("/songs/{song_id}", response_model=list[LinkResponse])
async def get_public_links(
    song_id: int,
    db: Session = Depends(get_session),
) -> list[DownloadLink]:
    """Get public download links for a song (no auth required)."""
    repo = SongRepository(db)
    if not repo.get_by_id(song_id):
        raise HTTPException(status_code=404, detail="Song not found")

    links = db.query(DownloadLink).filter(
        DownloadLink.song_id == song_id,
        DownloadLink.visibility == LinkVisibility.PUBLIC.value,
    ).all()

    # Redact private URLs as a safety measure
    for link in links:
        link.url = redact_private_urls(link.url)

    return links


@router.get("/admin/songs/{song_id}", response_model=list[LinkResponse])
async def get_all_links(
    song_id: int,
    db: Session = Depends(get_session),
    _: dict = Depends(require_admin),
) -> list[DownloadLink]:
    """Get all download links for a song (admin only)."""
    repo = SongRepository(db)
    if not repo.get_by_id(song_id):
        raise HTTPException(status_code=404, detail="Song not found")

    return db.query(DownloadLink).filter(DownloadLink.song_id == song_id).all()


@router.post("/admin", response_model=LinkResponse)
async def create_link(
    req: CreateLinkRequest,
    db: Session = Depends(get_session),
    _: dict = Depends(require_admin),
) -> DownloadLink:
    """Create a new download link (admin only)."""
    repo = SongRepository(db)
    if not repo.get_by_id(req.song_id):
        raise HTTPException(status_code=404, detail="Song not found")

    link = DownloadLink(
        song_id=req.song_id,
        label=req.label,
        url=req.url,
        link_type=req.link_type,
        visibility=req.visibility,
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@router.patch("/admin/{link_id}", response_model=LinkResponse)
async def update_link(
    link_id: int,
    req: UpdateLinkRequest,
    db: Session = Depends(get_session),
    _: dict = Depends(require_admin),
) -> DownloadLink:
    """Update a download link (admin only)."""
    link = db.query(DownloadLink).filter(DownloadLink.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    update_data = req.dict(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(link, key):
            setattr(link, key, value)

    db.commit()
    db.refresh(link)
    return link


@router.delete("/admin/{link_id}")
async def delete_link(
    link_id: int,
    db: Session = Depends(get_session),
    _: dict = Depends(require_admin),
) -> dict:
    """Delete a download link (admin only)."""
    link = db.query(DownloadLink).filter(DownloadLink.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    db.delete(link)
    db.commit()
    return {"deleted": True}
