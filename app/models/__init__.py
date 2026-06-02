"""Database models."""
from app.models.admin import AdminAuditLog, ExternalSource, SearchEvent
from app.models.links import DownloadLink, LinkType, LinkVisibility
from app.models.lyrics import LyricsSnippet
from app.models.media import CoverArt, MediaReference, MegaFileReference
from app.models.session_model import RecordingSession
from app.models.song import (
    Alias,
    DownloadStatus,
    Era,
    Producer,
    ReleaseStatus,
    Song,
    SongReference,
    SongVersion,
)

__all__ = [
    "Song",
    "Alias",
    "Era",
    "Producer",
    "ReleaseStatus",
    "DownloadStatus",
    "RecordingSession",
    "LyricsSnippet",
    "CoverArt",
    "MediaReference",
    "MegaFileReference",
    "ExternalSource",
    "SearchEvent",
    "AdminAuditLog",
    "DownloadLink",
    "LinkVisibility",
    "LinkType",
    "SongVersion",
    "SongReference",
]
