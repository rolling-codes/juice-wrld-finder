"""Era repository for database operations."""
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models import Era


class EraRepository:
    """Repository for era CRUD operations."""

    def __init__(self, db: Session) -> None:
        """Initialize with database session."""
        self.db = db

    def get_by_id(self, era_id: int) -> Optional[Era]:
        """Get era by ID."""
        return self.db.query(Era).filter(Era.id == era_id).first()

    def get_by_name(self, name: str) -> Optional[Era]:
        """Get era by name."""
        return self.db.query(Era).filter(Era.name == name).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Era]:
        """Get all eras with pagination."""
        return self.db.query(Era).offset(skip).limit(limit).all()

    def create(self, name: str, years: Optional[str] = None, description: Optional[str] = None) -> Era:
        """Create a new era."""
        era = Era(name=name, years=years, description=description)
        self.db.add(era)
        self.db.commit()
        self.db.refresh(era)
        return era

    def update(self, era_id: int, **kwargs: any) -> Optional[Era]:
        """Update an era."""
        era = self.get_by_id(era_id)
        if not era:
            return None
        for key, value in kwargs.items():
            if hasattr(era, key):
                setattr(era, key, value)
        self.db.commit()
        self.db.refresh(era)
        return era

    def delete(self, era_id: int) -> bool:
        """Delete an era."""
        era = self.get_by_id(era_id)
        if not era:
            return False
        self.db.delete(era)
        self.db.commit()
        return True
