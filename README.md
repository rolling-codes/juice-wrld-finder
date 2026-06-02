# Juice WRLD Metadata Finder

A Discord bot, web app, and FastAPI backend for searching and organizing Juice WRLD song metadata. This project indexes released and unreleased songs, eras, producers, and related metadata, with a public-facing gallery and admin panel for link management.

**This project is a metadata discovery platform, not a file distribution service.**

---

## ⚠️ Disclaimer

This project is fan-made and not affiliated with Juice WRLD, his estate, or any label. Use responsibly and respectfully.

**This project includes a connection to the Juice WRLD community API.**

**rolling-codes is not responsible for:**
- Any software downloads or file distribution via this tool or connected APIs
- Any copyright infringement or unauthorized distribution
- Any leaks or unauthorized sharing of copyrighted material
- Any misuse of the Juice WRLD community API

Users bear full responsibility for complying with copyright laws and the terms of service of any APIs used. The Juice WRLD community API integration is provided as-is for metadata purposes only.

For official Juice WRLD music, visit [streaming platforms](https://open.spotify.com/artist/4MCBfE4596Uoi2O4DtmHO1).

---

## Version History

### V1 (Current)

**What it is:**
- Fully-functional FastAPI metadata backend with 12 database models and 17 API endpoints
- Discord bot with search, era browsing, random song selection, and admin commands
- SQLite database with comprehensive music metadata schema
- CSV/JSON bulk import tooling for easy data seeding

**In Scope:**
- Core metadata models (songs, aliases, eras, producers, sessions, lyrics, cover art, media references)
- Full-text + fuzzy search with RapidFuzz
- MEGA folder integration (indexing only, no downloads)
- Juice WRLD community API integration (optional)
- Discord bot with metadata commands + admin tools
- 90%+ test coverage with pytest
- Docker Compose setup (SQLite, Redis, bot, API)
- GitHub Actions CI pipeline (ruff, mypy, pytest)
- Complete documentation

**Out of Scope (V1):**
- Web UI (public gallery, admin panel) — coming in V2
- Authentication/authorization — coming in V2
- Download link management — coming in V2
- PostgreSQL migration (phase 2 infrastructure)

**Deployment:** Local development or Docker Compose. Not production-ready yet (SQLite, no auth).

---

### V2 (Planned)

- React SPA public gallery + admin panel
- JWT auth for admin operations
- API key auth for bot HTTP requests
- Download link visibility model (public/bot/admin)
- New routes: `/auth/login`, `/links` (CRUD), `/bot/*`
- Security hardening: protected admin routes, CORS config
- OAuth2 / OAuth2PasswordBearer flow
- Better error handling and validation

---

## Features

- 🔍 **Fast Search** — Full-text + fuzzy search across song titles, aliases, and producers
- 🤖 **Discord Bot** — Native Discord slash commands for instant metadata lookups
- 🌐 **REST API** — FastAPI backend for programmatic access
- 🎵 **Comprehensive Metadata** — Songs, eras, producers, sessions, lyrics, cover art
- 🔐 **Safe By Default** — Controlled download link exposure via environment flags
- 📊 **Admin Tools** — CSV/JSON import, MEGA folder indexing, manual edits
- 🧪 **90%+ Test Coverage** — Production-ready test suite

## Installation Guides

Choose your deployment scenario below. All require Python 3.11+ and a cloned repository.

### Setup: Clone and Install Dependencies

```bash
git clone https://github.com/rolling-codes/juice-wrld-finder.git
cd juice-wrld-finder
pip install -r requirements.txt
```

---

### Option 1: Web App Only (No Discord)

Use this if you want the public gallery + admin panel without the Discord bot.

**Configure `.env`:**
```env
SECRET_KEY=your_secret_key_here
CORS_ORIGINS=["http://localhost:5173"]
DATABASE_URL=sqlite:///./juice_wrld.db
```

**Run:**
```bash
# Terminal 1: Backend API (port 8000)
python -c "from app.db import Base, engine; Base.metadata.create_all(bind=engine)"
uvicorn app.main:app --reload

# Terminal 2: Frontend (port 5173)
cd web
npm install
npm run dev
```

**Access:**
- Web app: http://localhost:5173
- API docs: http://localhost:8000/docs

---

### Option 2: Discord Bot Only (No Web App)

Use this if you want just the Discord bot with backend metadata, no web interface.

**Configure `.env`:**
```env
DISCORD_TOKEN=your_bot_token
DISCORD_GUILD_ID=your_guild_id
ADMIN_ROLE_ID=your_admin_role_id
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///./juice_wrld.db
# Optional: for download link visibility
EXPOSE_API_DOWNLOAD_LINKS=true
EXPOSE_MEGA_LINKS=false
```

**Run:**
```bash
# Terminal 1: Backend API (port 8000)
python -c "from app.db import Base, engine; Base.metadata.create_all(bind=engine)"
uvicorn app.main:app --reload

# Terminal 2: Discord Bot
python -m app.bot.client
```

**Use in Discord:**
- `/jw search <query>` — Search songs
- `/jw song <id>` — Get song details
- `/jw era <era_name>` — Browse by era
- `/jw random` — Random song

---

### Option 3: Full Stack (Web App + Discord Bot)

Use this for complete functionality: web gallery, admin panel, and Discord integration.

**Configure `.env`:**
```env
# Discord
DISCORD_TOKEN=your_bot_token
DISCORD_GUILD_ID=your_guild_id
ADMIN_ROLE_ID=your_admin_role_id

# Web App
SECRET_KEY=your_secret_key_here
CORS_ORIGINS=["http://localhost:5173"]
DATABASE_URL=sqlite:///./juice_wrld.db

# Optional Downloads
EXPOSE_API_DOWNLOAD_LINKS=true
EXPOSE_MEGA_LINKS=false
```

**Run:**
```bash
# Terminal 1: Backend API (port 8000)
python -c "from app.db import Base, engine; Base.metadata.create_all(bind=engine)"
uvicorn app.main:app --reload

# Terminal 2: Discord Bot
python -m app.bot.client

# Terminal 3: Frontend (port 5173)
cd web
npm install
npm run dev
```

**Access:**
- Web app: http://localhost:5173
- Discord commands: `/jw ...`
- API docs: http://localhost:8000/docs

---

### Import Initial Data

Prepare a CSV file with columns: `title`, `era`, `release_status`, `download_status`, `official_url`, `api_download_url`, `notes`, `aliases`, `producers`

```bash
python scripts/import_csv.py songs.csv
```

## Commands

### User Commands

- `/jw search <query>` — Search songs by title, alias, or keyword
- `/jw song <id>` — Get full metadata for a song
- `/jw era <era_name>` — List songs from an era
- `/jw random` — Get a random song
- `/jw lyrics <phrase>` — Search indexed lyric snippets

### Admin Commands (requires `ADMIN_ROLE_ID`)

- `/jw admin add-song <title>` — Add a new song
- `/jw admin edit-song <id> <updates>` — Edit song metadata
- `/jw admin remove-song <id>` — Delete a song
- `/jw admin reindex` — Reindex MEGA folders

## API Endpoints

```
GET  /health                    # Health check
GET  /songs                     # List songs
GET  /songs/{id}                # Get song details
GET  /search?q=<query>          # Search songs
GET  /search/lyrics?q=<phrase>  # Search lyrics
GET  /eras                      # List eras
GET  /eras/{id}/songs           # Songs from era
GET  /producers                 # List producers

POST   /admin/songs             # Create song
PATCH  /admin/songs/{id}        # Update song
DELETE /admin/songs/{id}        # Delete song
```

## Configuration

### Feature Flags

```env
EXPOSE_API_DOWNLOAD_LINKS=false   # Show Juice WRLD API download links
EXPOSE_MEGA_LINKS=false           # Show MEGA folder download links
```

### MEGA Folders

Configure these in `.env` to enable MEGA indexing:

```env
MEGA_MAIN_COMP=https://mega.nz/folder/...
MEGA_ERA_COMP=https://mega.nz/folder/...
MEGA_COVER_ART_COMP=https://mega.nz/folder/...
MEGA_MEDIA_COMP=https://mega.nz/folder/...
MEGA_SESSION_EDITS_COMP=https://mega.nz/folder/...
```

## Data Sources

This project uses publicly available metadata from:

1. **Official Releases** — Spotify, Apple Music, YouTube
2. **Juiceboard API** — https://juicewrldapi.com (Juice WRLD community API)
3. **User-Submitted Data** — Via CSV/JSON import
4. **MEGA Folder References** — Filename indexing only (no downloads)

See [docs/REFERENCE_LINKS.md](docs/REFERENCE_LINKS.md) and [docs/API_SOURCES.md](docs/API_SOURCES.md) for details.

## Features

✅ **Direct External Links** — Links to Juiceboard API and MEGA (no proxying)
✅ **Controlled link exposure** — Download URLs only shown if explicitly enabled
✅ **URL redaction** — Private file-hosting links redacted from bot responses
✅ **Admin-only operations** — Sensitive commands require role verification
✅ **Audit logging** — All admin actions logged

## Testing

Run the full test suite:

```bash
pytest --cov=app --cov-report=term-missing
```

Linting and type checking:

```bash
ruff check .
mypy app
```

See [docs/TESTING.md](docs/TESTING.md) for detailed testing guide.

## Deployment

### Docker Compose (Local)

```bash
docker-compose up --build
```

This starts:
- API on port 8000
- Bot (connects to Discord)
- Redis on port 6379
- SQLite database

### Production (VPS)

For Railway, Fly.io, or similar:

1. Set environment variables
2. Build Docker image
3. Deploy with persistent database volume
4. Use PostgreSQL + Redis instead of SQLite

See `docker-compose.yml` for the services definition.

## Project Structure

```
juice-wrld-finder/
├── app/
│   ├── api/          # FastAPI routes
│   ├── bot/          # Discord bot + cogs
│   ├── core/         # Config, security
│   ├── db/           # SQLAlchemy setup
│   ├── models/       # Database models
│   ├── repositories/ # Data access layer
│   ├── services/     # Business logic
│   └── integrations/ # External APIs (Juice WRLD, MEGA)
├── scripts/          # CSV importer, utilities
├── tests/            # Pytest test suite
├── docs/             # Documentation
├── Dockerfile        # Container image
└── docker-compose.yml
```

## Development

Clone, install, and run locally:

```bash
git clone <repo>
cd juice-wrld-finder
pip install -r requirements.txt

# Terminal 1: API
uvicorn app.main:app --reload

# Terminal 2: Bot
python -m app.bot.client
```

Changes auto-reload in both processes.

## API Integration Note

This project integrates with the **Juiceboard API** ([https://juicewrldapi.com/](https://juicewrldapi.com/)) which may provide download links for songs. This tool is designed for **metadata discovery and organization only**. 

**Disclaimer:** This project includes a reference to the Juiceboard API that *can* be used to download songs, but **the rolling-codes team does not advise or endorse any software downloads or distribution**. Users are solely responsible for complying with copyright laws and the terms of service of any APIs used. **rolling-codes is not responsible for any downloads, leaks, or unauthorized distribution of copyrighted material.** Only download songs you have permission to download. Support the artist by using official streaming platforms when available.

## License

MIT

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new code
4. Ensure 90%+ coverage
5. Submit a pull request

All tests and linting must pass (see GitHub Actions).
