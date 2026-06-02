"""Bot API routes for Discord bot integration."""

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_session
from app.core.auth import require_bot
from app.models import DownloadLink, LinkVisibility, Song
from app.repositories import SongRepository

router = APIRouter(prefix="/bot", tags=["bot"])


class BotLinkResponse(BaseModel):
    """Link response for bot."""
    id: int
    label: str
    url: str
    link_type: str

    class Config:
        from_attributes = True


class BotSongResponse(BaseModel):
    """Song response for bot."""
    id: int
    title: str
    slug: str
    release_status: str
    download_status: str
    links: list[BotLinkResponse]

    class Config:
        from_attributes = True


@router.get("/songs", response_model=list[BotSongResponse])
async def get_bot_songs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
    x_api_key: str = Header(...),
) -> list[dict]:
    """Get all songs with public/bot links (requires bot API key)."""
    await require_bot(x_api_key)

    songs = db.query(Song).offset(skip).limit(limit).all()
    result = []

    for song in songs:
        links = db.query(DownloadLink).filter(
            DownloadLink.song_id == song.id,
            DownloadLink.visibility.in_([LinkVisibility.PUBLIC, LinkVisibility.BOT]),
        ).all()

        result.append({
            "id": song.id,
            "title": song.title,
            "slug": song.slug,
            "release_status": song.release_status,
            "download_status": song.download_status,
            "links": [
                {
                    "id": link.id,
                    "label": link.label,
                    "url": link.url,
                    "link_type": link.link_type,
                }
                for link in links
            ],
        })

    return result


@router.get("/songs/{song_id}/links", response_model=list[BotLinkResponse])
async def get_bot_song_links(
    song_id: int,
    db: Session = Depends(get_session),
    x_api_key: str = Header(...),
) -> list[DownloadLink]:
    """Get public/bot links for a song (requires bot API key)."""
    await require_bot(x_api_key)

    repo = SongRepository(db)
    if not repo.get_by_id(song_id):
        raise HTTPException(status_code=404, detail="Song not found")

    return db.query(DownloadLink).filter(
        DownloadLink.song_id == song_id,
        DownloadLink.visibility.in_([LinkVisibility.PUBLIC, LinkVisibility.BOT]),
    ).all()
