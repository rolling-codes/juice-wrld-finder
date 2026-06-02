"""MEGA folder indexer for song discovery."""
import logging
from typing import Optional

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import MegaFileReference

logger = logging.getLogger(__name__)


class MEGAIndexer:
    """Index MEGA folder contents for song matching."""

    MATCH_THRESHOLD = 70

    def __init__(self, db: Session) -> None:
        """Initialize with database session."""
        self.db = db
        self.folders = {
            "main_comp": settings.mega_main_comp,
            "era_comp": settings.mega_era_comp,
            "cover_art_comp": settings.mega_cover_art_comp,
            "media_comp": settings.mega_media_comp,
            "session_edits_comp": settings.mega_session_edits_comp,
        }

    def index_folders(self) -> dict:
        """Index all configured MEGA folders (placeholder for phase 2)."""
        stats = {
            "indexed": 0,
            "matched": 0,
            "errors": 0,
        }

        for folder_name, folder_url in self.folders.items():
            if not folder_url:
                continue

            logger.info(f"Indexing {folder_name}: {folder_url}")

            # Phase 2: Implement mega.py integration
            # For now, just log the configuration
            logger.info(f"MEGA indexing for {folder_name} would happen here")

        return stats

    def match_files_to_songs(self) -> dict:
        """Match indexed MEGA files to songs in database."""
        stats = {
            "matched": 0,
            "unmatched": 0,
        }

        # Phase 2: Implement matching logic using fuzzy search
        # For now, placeholder

        return stats

    def get_mega_link_for_song(self, song_id: int) -> Optional[str]:
        """Get MEGA download link for a song if available."""
        if not settings.expose_mega_links:
            return None

        ref = self.db.query(MegaFileReference).filter(
            MegaFileReference.song_id == song_id,
        ).first()

        if ref:
            return ref.mega_url

        return None
