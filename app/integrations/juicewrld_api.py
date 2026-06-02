"""Juice WRLD API client."""
from typing import Optional, List, Any
import httpx
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class JuiceWRLDAPIClient:
    """Async client for Juice WRLD community API."""

    def __init__(self) -> None:
        """Initialize API client."""
        self.base_url = settings.juicewrld_api_base
        self.timeout = 10.0

    async def search_songs(self, query: str, limit: int = 20) -> List[dict]:
        """Search for songs."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(
                    f"{self.base_url}/search",
                    params={"q": query, "limit": limit},
                )
                resp.raise_for_status()
                return resp.json().get("results", [])
            except httpx.HTTPError as e:
                logger.error(f"API search error: {e}")
                return []

    async def get_song(self, song_id: str) -> Optional[dict]:
        """Get a specific song."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/songs/{song_id}")
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPError as e:
                logger.error(f"API get_song error: {e}")
                return None

    async def get_songs(self, skip: int = 0, limit: int = 50) -> List[dict]:
        """Get all songs with pagination."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(
                    f"{self.base_url}/songs",
                    params={"skip": skip, "limit": limit},
                )
                resp.raise_for_status()
                return resp.json().get("results", [])
            except httpx.HTTPError as e:
                logger.error(f"API get_songs error: {e}")
                return []

    async def get_eras(self) -> List[dict]:
        """Get all eras."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/eras")
                resp.raise_for_status()
                return resp.json().get("results", [])
            except httpx.HTTPError as e:
                logger.error(f"API get_eras error: {e}")
                return []

    async def get_producers(self) -> List[dict]:
        """Get all producers."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/producers")
                resp.raise_for_status()
                return resp.json().get("results", [])
            except httpx.HTTPError as e:
                logger.error(f"API get_producers error: {e}")
                return []
