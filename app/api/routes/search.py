"""Search routes."""
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.api.deps import get_session
from app.services import SearchService, SearchResult

router = APIRouter(prefix="/search", tags=["search"])


class SearchResultResponse(BaseModel):
    """Search result response."""

    id: int
    title: str
    confidence: float

    class Config:
        """Pydantic config."""
        from_attributes = True


@router.get("", response_model=List[SearchResultResponse])
async def search(
    q: str = Query(..., min_length=1, description="Search query"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_session),
) -> List[dict]:
    """Search songs by title or alias."""
    service = SearchService(db)
    results = service.search(q, skip=skip, limit=limit)
    return [r.to_dict() for r in results]


@router.get("/lyrics", response_model=List[SearchResultResponse])
async def search_lyrics(
    q: str = Query(..., min_length=1, description="Lyric phrase"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_session),
) -> List[dict]:
    """Search by lyric snippets."""
    service = SearchService(db)
    results = service.search_by_lyrics(q, skip=skip, limit=limit)
    return [{"id": s.id, "title": s.title, "confidence": 1.0} for s in results]
