"""Search repository for complex search operations."""
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import Alias, Song
from app.models.lyrics import LyricsSnippet
from app.models.song import Producer


class SearchRepository:
    """Repository for advanced search operations."""

    def __init__(self, db: Session) -> None:
        """Initialize with database session."""
        self.db = db

    def full_text_search(self, query: str, skip: int = 0, limit: int = 50) -> list[Song]:
        """Perform full-text search across titles and aliases."""
        query_lower = query.lower().strip()
        if not query_lower:
            return []

        results = self.db.query(Song).join(
            Alias, Song.id == Alias.song_id, isouter=True
        ).filter(
            or_(
                Song.title.ilike(f"%{query_lower}%"),
                Alias.alias.ilike(f"%{query_lower}%"),
                Song.notes.ilike(f"%{query_lower}%")
            )
        ).offset(skip).limit(limit).all()

        return results

    def search_by_producer(self, producer_name: str, skip: int = 0, limit: int = 50) -> list[Song]:
        """Search songs by producer name."""
        producer_lower = producer_name.lower()
        return self.db.query(Song).filter(
            Song.producers.any(Producer.name.ilike(f"%{producer_lower}%"))
        ).offset(skip).limit(limit).all()

    def get_random_song(self, filters: Optional[dict] = None) -> Optional[Song]:
        """Get a random song, optionally filtered by release/download status."""
        query = self.db.query(Song)

        if filters:
            if filters.get("released"):
                query = query.filter(Song.release_status == "released")
            elif filters.get("unreleased"):
                query = query.filter(Song.release_status == "unreleased")

            if filters.get("metadata_only"):
                query = query.filter(Song.download_status == "metadata_only")

            if filters.get("official_release_available"):
                query = query.filter(Song.download_status == "official_release_available")

        song = query.order_by("RANDOM()").first()
        return song

    def search_lyrics(self, phrase: str, skip: int = 0, limit: int = 50) -> list[Song]:
        """Search songs by lyric snippets."""
        phrase_lower = phrase.lower()
        return self.db.query(Song).filter(
            Song.lyrics.any(LyricsSnippet.snippet_text.ilike(f"%{phrase_lower}%"))
        ).offset(skip).limit(limit).all()
