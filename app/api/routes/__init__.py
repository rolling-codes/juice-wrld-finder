"""API routes."""
from app.api.routes import admin, auth, bot, eras, health, links, producers, search, songs

__all__ = ["health", "songs", "search", "eras", "producers", "admin", "auth", "links", "bot"]
