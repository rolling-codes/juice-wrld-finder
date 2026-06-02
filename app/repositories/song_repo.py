"""Song repository for database operations."""
from typing import Any, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import Alias, Song, SongReference, SongVersion


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

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Song]:
        """Get all songs with pagination."""
        return self.db.query(Song).offset(skip).limit(limit).all()

    def get_by_era_id(self, era_id: int, skip: int = 0, limit: int = 100) -> list[Song]:
        """Get songs from an era."""
        return self.db.query(Song).filter(Song.era_id == era_id).offset(skip).limit(limit).all()

    def get_by_release_status(self, status: str, skip: int = 0, limit: int = 100) -> list[Song]:
        """Get songs by release status."""
        return self.db.query(Song).filter(Song.release_status == status).offset(skip).limit(limit).all()

    def search_by_title_or_alias(self, query: str) -> list[Song]:
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

    def get_versions(self, song_id: int) -> list[SongVersion]:
        """Get stored song versions, with the base version first."""
        return (
            self.db.query(SongVersion)
            .filter(SongVersion.song_id == song_id)
            .order_by(
                SongVersion.is_base_version.desc(),
                SongVersion.sort_order.asc(),
                SongVersion.id.asc(),
            )
            .all()
        )

    def get_references(self, song_id: int) -> list[SongReference]:
        """Get non-download references for a song."""
        return (
            self.db.query(SongReference)
            .filter(SongReference.song_id == song_id)
            .order_by(SongReference.id.asc())
            .all()
        )

    def add_version(
        self,
        song_id: int,
        title: str,
        *,
        version_type: str = "released",
        release_status: str = "unknown",
        is_base_version: bool = False,
        recorded_date: str | None = None,
        surfaced_date: str | None = None,
        source_name: str | None = None,
        source_url: str | None = None,
        confidence: float = 1.0,
        sort_order: int = 0,
        notes: str | None = None,
    ) -> SongVersion:
        """Add a version to a song."""
        version = SongVersion(
            song_id=song_id,
            title=title,
            version_type=version_type,
            release_status=release_status,
            is_base_version=is_base_version,
            recorded_date=recorded_date,
            surfaced_date=surfaced_date,
            source_name=source_name,
            source_url=source_url,
            confidence=confidence,
            sort_order=sort_order,
            notes=notes,
        )
        self.db.add(version)
        self.db.commit()
        self.db.refresh(version)
        return version

    def add_reference(
        self,
        song_id: int,
        source_name: str,
        *,
        source_type: str = "manual",
        source_url: str | None = None,
        description: str | None = None,
        confidence: float = 1.0,
    ) -> SongReference:
        """Add a non-download reference to a song."""
        reference = SongReference(
            song_id=song_id,
            source_type=source_type,
            source_name=source_name,
            source_url=source_url,
            description=description,
            confidence=confidence,
        )
        self.db.add(reference)
        self.db.commit()
        self.db.refresh(reference)
        return reference

    def create(self, title: str, slug: str, release_status: str = "unknown", **kwargs: Any) -> Song:
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

    def update(self, song_id: int, **kwargs: Any) -> Optional[Song]:
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
