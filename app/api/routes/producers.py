"""Producer routes."""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.api.deps import get_session
from app.models import Producer

router = APIRouter(prefix="/producers", tags=["producers"])


class ProducerResponse(BaseModel):
    """Producer response model."""

    id: int
    name: str

    class Config:
        """Pydantic config."""
        from_attributes = True


@router.get("", response_model=List[ProducerResponse])
async def list_producers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
) -> List[Producer]:
    """List all producers."""
    producers = db.query(Producer).offset(skip).limit(limit).all()
    return producers
