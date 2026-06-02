"""FastAPI dependency injections."""
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import get_db


def get_session(db: Session = Depends(get_db)) -> Session:
    """Get database session."""
    return db
