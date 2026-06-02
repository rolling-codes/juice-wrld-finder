"""Business logic for song operations."""
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models import Song, Alias, Producer, Era
from app.repositories import SongRepository


class SongService:
    """Service layer for song operations."""

    def __init__(self, db: Session) -> None:
        """Initialize with database session."""
        self.db = db
        self.repo = SongRepository(db)

    def create_song(
        self,
        title: str,
        era_name: Optional[str] = None,
        release_status: str = "unknown",
        download_status: str = "metadata_only",
        **kwargs: any,
    ) -> Song:
        """Create a song with optional era assignment."""
        slug = self._create_slug(title)

        era = None
        if era_name:
            era = self.db.query(Era).filter(Era.name == era_name).first()
            if not era:
                era = Era(name=era_name)
                self.db.add(era)
                self.db.flush()

        song = self.repo.create(
            title=title,
            slug=slug,
            release_status=release_status,
            download_status=download_status,
            era_id=era.id if era else None,
            **kwargs,
        )
        return song

    def add_alias(self, song_id: int, alias: str) -> bool:
        """Add an alias to a song."""
        song = self.repo.get_by_id(song_id)
        if not song:
            return False

        existing = self.db.query(Alias).filter(
            Alias.song_id == song_id,
            Alias.alias == alias,
        ).first()
        if existing:
            return True

        new_alias = Alias(song_id=song_id, alias=alias)
        self.db.add(new_alias)
        self.db.commit()
        return True

    def add_producer(self, song_id: int, producer_name: str) -> bool:
        """Add or link a producer to a song."""
        song = self.repo.get_by_id(song_id)
        if not song:
            return False

        producer = self.db.query(Producer).filter(Producer.name == producer_name).first()
        if not producer:
            producer = Producer(name=producer_name)
            self.db.add(producer)
            self.db.flush()

        if producer not in song.producers:
            song.producers.append(producer)
            self.db.commit()

        return True

    def get_song_detail(self, song_id: int) -> Optional[Song]:
        """Get full song detail."""
        return self.repo.get_by_id(song_id)

    def _create_slug(self, title: str) -> str:
        """Generate a URL-safe slug from a title."""
        slug = title.lower().replace(" ", "-").replace(".", "").replace("'", "")
        slug = "".join(c for c in slug if c.isalnum() or c == "-")
        return slug
