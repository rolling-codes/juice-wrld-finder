"""FastAPI dependency injections."""
from sqlalchemy.orm import Session
from fastapi import Depends

from app.db import get_db


def get_session(db: Session = Depends(get_db)) -> Session:
    """Get database session."""
    return db
