"""FastAPI application factory."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    admin,
    auth,
    bot,
    downloads,
    eras,
    health,
    links,
    producers,
    search,
    songs,
)
from app.core.config import settings
from app.db import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Juice WRLD Metadata Finder",
    description="Discord bot, API, and web app for music metadata, release versions, references, and public link management",
    version="1.1.0",
)

# CORS middleware — allow specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(health.router)
app.include_router(songs.router)
app.include_router(search.router)
app.include_router(eras.router)
app.include_router(producers.router)
app.include_router(auth.router)
app.include_router(links.router)
app.include_router(downloads.router)
app.include_router(bot.router)
app.include_router(admin.router)


@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {"message": "Juice WRLD Metadata Finder API"}
