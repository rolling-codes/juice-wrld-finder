"""FastAPI application factory."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import Base, engine
from app.api.routes import health, songs, search, eras, producers, admin

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Juice WRLD Metadata Finder",
    description="Discord bot and API for searching Juice WRLD song metadata",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
app.include_router(admin.router)


@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {"message": "Juice WRLD Metadata Finder API"}
