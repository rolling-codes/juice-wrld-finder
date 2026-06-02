"""Song repository for database operations."""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models import Song, Alias, Era, Producer


class SongRepository:
    """Repository for song CRUD operations."""

    def __init__(self, db: Session) -> None:
        """Initialize with database session."""
        self.db = db

    def get_by_id(self, song_id: int) -> Optional[Song]:
        """Get song by ID."""
        return self.db.query(Song).filter(Song.id == song_id).first()

    def get_by_title(self, title: str) -> Optional[Song]:
        """Get song by exact title."""
        return self.db.query(Song).filter(Song.title == title).first()

    def get_by_slug(self, slug: str) -> Optional[Song]:
        """Get song by slug."""
        return self.db.query(Song).filter(Song.slug == slug).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Song]:
        """Get all songs with pagination."""
        return self.db.query(Song).offset(skip).limit(limit).all()

    def get_by_era_id(self, era_id: int, skip: int = 0, limit: int = 100) -> List[Song]:
        """Get songs from an era."""
        return self.db.query(Song).filter(Song.era_id == era_id).offset(skip).limit(limit).all()

    def get_by_release_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Song]:
        """Get songs by release status."""
        return self.db.query(Song).filter(Song.release_status == status).offset(skip).limit(limit).all()

    def search_by_title_or_alias(self, query: str) -> List[Song]:
        """Search songs by title or alias (case-insensitive)."""
        query_lower = query.lower()
        return self.db.query(Song).join(
            Alias, Song.id == Alias.song_id, isouter=True
        ).filter(
            or_(
                Song.title.ilike(f"%{query_lower}%"),
                Alias.alias.ilike(f"%{query_lower}%")
            )
        ).all()

    def create(self, title: str, slug: str, release_status: str = "unknown", **kwargs: any) -> Song:
        """Create a new song."""
        song = Song(
            title=title,
            slug=slug,
            release_status=release_status,
            **kwargs
        )
        self.db.add(song)
        self.db.commit()
        self.db.refresh(song)
        return song

    def update(self, song_id: int, **kwargs: any) -> Optional[Song]:
        """Update a song."""
        song = self.get_by_id(song_id)
        if not song:
            return None
        for key, value in kwargs.items():
            if hasattr(song, key):
                setattr(song, key, value)
        self.db.commit()
        self.db.refresh(song)
        return song

    def delete(self, song_id: int) -> bool:
        """Delete a song."""
        song = self.get_by_id(song_id)
        if not song:
            return False
        self.db.delete(song)
        self.db.commit()
        return True

    def count(self) -> int:
        """Count total songs."""
        return self.db.query(Song).count()
