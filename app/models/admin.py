"""Admin audit and search logging models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text

from app.db.base import Base


class ExternalSource(Base):
    """External data source metadata."""
    __tablename__ = "external_source"

    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey("song.id"), nullable=False)
    source_name = Column(String(100), nullable=False)
    source_url = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class SearchEvent(Base):
    """Search query logging for analytics."""
    __tablename__ = "search_event"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String(255), nullable=False)
    results_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class AdminAuditLog(Base):
    """Admin action audit trail."""
    __tablename__ = "admin_audit_log"

    id = Column(Integer, primary_key=True, index=True)
    admin_user_id = Column(Integer, nullable=False)
    action = Column(String(100), nullable=False)
    target_id = Column(Integer, nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
