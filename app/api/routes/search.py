"""Search routes."""

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_session
from app.services import SearchService

router = APIRouter(prefix="/search", tags=["search"])


class SearchResultResponse(BaseModel):
    """Search result response."""

    id: int
    title: str
    slug: str | None = None
    release_status: str | None = None
    download_status: str | None = None
    official_url: str | None = None
    notes: str | None = None
    era_id: int | None = None
    version_count: int = 0
    reference_count: int = 0
    source_names: list[str] = Field(default_factory=list)
    confidence: float

    class Config:
        """Pydantic config."""
        from_attributes = True


@router.get("", response_model=list[SearchResultResponse])
async def search(
    q: str = Query(..., min_length=1, description="Search query"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_session),
) -> list[dict]:
    """Search songs by title or alias."""
    service = SearchService(db)
    results = service.search(q, skip=skip, limit=limit)
    return [r.to_dict() for r in results]


@router.get("/lyrics", response_model=list[SearchResultResponse])
async def search_lyrics(
    q: str = Query(..., min_length=1, description="Lyric phrase"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_session),
) -> list[dict]:
    """Search by lyric snippets."""
    service = SearchService(db)
    results = service.search_by_lyrics(q, skip=skip, limit=limit)
    return [
        {
            "id": s.id,
            "title": s.title,
            "slug": s.slug,
            "release_status": s.release_status,
            "download_status": s.download_status,
            "official_url": s.official_url,
            "notes": s.notes,
            "era_id": s.era_id,
            "version_count": len(s.versions),
            "reference_count": len(s.references),
            "source_names": sorted(
                {
                    reference.source_name
                    for reference in s.references
                    if reference.source_name
                }
            ),
            "confidence": 1.0,
        }
        for s in results
    ]
