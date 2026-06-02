"""Download link model."""
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class LinkVisibility(str, Enum):
    """Link visibility control."""
    PUBLIC = "public"      # Shown on public gallery, bot, admin
    BOT = "bot"            # Bot + admin only
    ADMIN = "admin"        # Admin only


class LinkType(str, Enum):
    """Type of download link."""
    MEGA = "mega"
    API = "api"
    OFFICIAL = "official"
    OTHER = "other"


class DownloadLink(Base):
    """Download link metadata and visibility control."""
    __tablename__ = "download_link"

    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey("song.id"), nullable=False, index=True)
    label = Column(String(100), nullable=False)
    url = Column(Text, nullable=False)
    link_type = Column(String(20), default=LinkType.OTHER.value, nullable=False)
    visibility = Column(String(20), default=LinkVisibility.BOT.value, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    song = relationship("Song", back_populates="download_links")
