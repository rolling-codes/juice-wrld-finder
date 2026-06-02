"""Test fixtures and configuration."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.core.config import settings


@pytest.fixture
def db() -> Session:
    """Create a test database session using SQLite in-memory."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def override_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    """Override settings for testing."""
    monkeypatch.setattr("app.core.config.settings.expose_api_download_links", False)
    monkeypatch.setattr("app.core.config.settings.expose_mega_links", False)
