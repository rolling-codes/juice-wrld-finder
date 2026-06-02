"""Download routes - redirect to external sources."""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.api.deps import get_session
from app.repositories import LinkRepository, SongRepository

router = APIRouter(prefix="/downloads", tags=["downloads"])


@router.get("/{song_id}")
async def download_song(
    song_id: int,
    link_id: int | None = None,
    db: Session = Depends(get_session),
):
    """Download a song by redirecting to external source.

    If link_id is provided, download that specific link.
    Otherwise, return the first available PUBLIC link.
    """
    song_repo = SongRepository(db)
    link_repo = LinkRepository(db)

    song = song_repo.get_by_id(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    if link_id:
        link = link_repo.get_by_id(link_id)
        if not link or link.song_id != song_id:
            raise HTTPException(status_code=404, detail="Download link not found")
        if link.visibility != "PUBLIC":
            raise HTTPException(status_code=403, detail="Link not publicly available")
        return RedirectResponse(url=link.url)

    links = link_repo.get_public_links_for_song(song_id)
    if not links:
        raise HTTPException(
            status_code=404,
            detail=f"No download links available for {song.title}",
        )

    return RedirectResponse(url=links[0].url)
