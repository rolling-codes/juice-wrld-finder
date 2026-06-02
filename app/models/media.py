"""Media reference models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class CoverArt(Base):
    """Cover art metadata."""
    __tablename__ = "cover_art"

    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey("song.id"), nullable=False)
    description = Column(String(255), nullable=True)
    official_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    song = relationship("Song", back_populates="cover_art")


class MediaReference(Base):
    """External media references."""
    __tablename__ = "media_reference"

    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey("song.id"), nullable=False)
    platform = Column(String(100), nullable=False)
    url = Column(Text, nullable=False)
    media_type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    song = relationship("Song", back_populates="media_references")


class MegaFileReference(Base):
    """MEGA folder file indexing."""
    __tablename__ = "mega_file_reference"

    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey("song.id"), nullable=True)
    mega_url = Column(Text, nullable=False)
    folder_label = Column(String(100), nullable=False)
    filename = Column(String(255), nullable=False, index=True)
    matched_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    song = relationship("Song", back_populates="mega_files")
