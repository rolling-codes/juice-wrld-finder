"""Song and related models."""
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class ReleaseStatus(str, Enum):
    """Song release status."""
    RELEASED = "released"
    UNRELEASED = "unreleased"
    UNKNOWN = "unknown"


class DownloadStatus(str, Enum):
    """Download availability status."""
    NOT_AVAILABLE = "not_available"
    OFFICIAL_RELEASE_AVAILABLE = "official_release_available"
    PREVIEW_ONLY = "preview_only"
    METADATA_ONLY = "metadata_only"
    USER_OWNED_FILE_REFERENCE = "user_owned_file_reference"
    API_LINK_AVAILABLE = "api_link_available"


song_producer_association = Table(
    "song_producer",
    Base.metadata,
    Column("song_id", Integer, ForeignKey("song.id"), primary_key=True),
    Column("producer_id", Integer, ForeignKey("producer.id"), primary_key=True),
)


class Song(Base):
    """Song metadata."""
    __tablename__ = "song"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, index=True, nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    release_status = Column(String(20), default=ReleaseStatus.UNKNOWN.value, nullable=False)
    download_status = Column(String(50), default=DownloadStatus.METADATA_ONLY.value, nullable=False)
    api_download_url = Column(Text, nullable=True)
    official_url = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    era_id = Column(Integer, ForeignKey("era.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    aliases = relationship("Alias", back_populates="song", cascade="all, delete-orphan")
    producers = relationship("Producer", secondary=song_producer_association)
    sessions = relationship("RecordingSession", back_populates="song", cascade="all, delete-orphan")
    lyrics = relationship("LyricsSnippet", back_populates="song", cascade="all, delete-orphan")
    cover_art = relationship("CoverArt", back_populates="song", cascade="all, delete-orphan")
    media_references = relationship("MediaReference", back_populates="song", cascade="all, delete-orphan")
    external_sources = relationship("ExternalSource", back_populates="song", cascade="all, delete-orphan")
    mega_files = relationship("MegaFileReference", back_populates="song", cascade="all, delete-orphan")
    download_links = relationship("DownloadLink", back_populates="song", cascade="all, delete-orphan")
    versions = relationship("SongVersion", back_populates="song", cascade="all, delete-orphan")
    references = relationship("SongReference", back_populates="song", cascade="all, delete-orphan")
    era = relationship("Era", back_populates="songs")


class Alias(Base):
    """Alternative song titles."""
    __tablename__ = "alias"
    __table_args__ = (UniqueConstraint("song_id", "alias", name="uq_song_alias"),)

    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey("song.id"), nullable=False)
    alias = Column(String(255), index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    song = relationship("Song", back_populates="aliases")


class Era(Base):
    """Music era/period."""
    __tablename__ = "era"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    years = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    songs = relationship("Song", back_populates="era")


class Producer(Base):
    """Music producer."""
    __tablename__ = "producer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class SongVersion(Base):
    """Alternate or known versions of a song."""
    __tablename__ = "song_version"
    __table_args__ = (UniqueConstraint("song_id", "title", "version_type", name="uq_song_version"),)

    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey("song.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    version_type = Column(String(50), default="released", nullable=False)
    release_status = Column(String(20), default=ReleaseStatus.UNKNOWN.value, nullable=False)
    is_base_version = Column(Boolean, default=False, nullable=False)
    recorded_date = Column(String(50), nullable=True)
    surfaced_date = Column(String(50), nullable=True)
    source_name = Column(String(100), nullable=True)
    source_url = Column(Text, nullable=True)
    confidence = Column(Float, default=1.0, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    song = relationship("Song", back_populates="versions")


class SongReference(Base):
    """Non-download reference links for song metadata."""
    __tablename__ = "song_reference"

    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey("song.id"), nullable=False, index=True)
    source_type = Column(String(50), default="manual", nullable=False)
    source_name = Column(String(100), nullable=False)
    source_url = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    confidence = Column(Float, default=1.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    song = relationship("Song", back_populates="references")
