"""Lyrics snippet model."""
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class LyricsSnippet(Base):
    """Indexed lyric snippets."""
    __tablename__ = "lyrics_snippet"

    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey("song.id"), nullable=False)
    snippet_text = Column(Text, nullable=False)
    source = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    song = relationship("Song", back_populates="lyrics")
