"""Download link repository for database operations."""
from sqlalchemy.orm import Session

from app.models import DownloadLink, LinkVisibility


class LinkRepository:
    """Repository for download link CRUD operations."""

    def __init__(self, db: Session) -> None:
        """Initialize with database session."""
        self.db = db

    def get_by_id(self, link_id: int) -> DownloadLink | None:
        """Get a download link by ID."""
        return self.db.query(DownloadLink).filter(DownloadLink.id == link_id).first()

    def get_public_links_for_song(self, song_id: int) -> list[DownloadLink]:
        """Get public download links for a song."""
        return (
            self.db.query(DownloadLink)
            .filter(
                DownloadLink.song_id == song_id,
                DownloadLink.visibility == LinkVisibility.PUBLIC.value,
            )
            .all()
        )
