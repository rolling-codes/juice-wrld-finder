# API Sources and Data Integration

This document describes the external data sources used by the Juice WRLD Metadata Finder.

## Juiceboard API

**Official:** Unofficial / Community-maintained  
**Also known as:** Juice WRLD Community API

**Base URL:** `https://juicewrldapi.com/api`

**Docs:** https://juicewrldapi.com/docs

### Supported Endpoints

- `GET /songs` — Get all songs with pagination
- `GET /songs/{id}` — Get a specific song
- `GET /search?q={query}` — Search songs
- `GET /eras` — Get all eras
- `GET /categories` — Get song categories
- `GET /producers` — Get all producers
- `GET /statistics` — Get general stats

### Implementation

The API client is at `app/integrations/juicewrld_api.py` using `httpx` for async requests.

```python
from app.integrations import JuiceWRLDAPIClient

client = JuiceWRLDAPIClient()
songs = await client.search_songs("lucid dreams")
```

### Download Links

The API may return `download_url` fields in song objects. These are **gated by the `EXPOSE_API_DOWNLOAD_LINKS` environment flag**.

- When `EXPOSE_API_DOWNLOAD_LINKS=false` (default): Download URLs are stored in the database but never returned to users.
- When `EXPOSE_API_DOWNLOAD_LINKS=true`: Download URLs are included in bot and API responses.

### Limitations

- Community-maintained (subject to changes)
- No official support
- May include inaccurate data
- Always verify critical metadata

## MEGA Folder Integration

**Service:** MEGA cloud storage (user-provided links)

**Folders:** Five manually-configured MEGA folder links

### Implementation

The MEGA indexer is at `app/integrations/mega_indexer.py` using the `mega.py` library.

**What it does:**
- Enumerates folder contents (no file downloads)
- Extracts filenames and download links
- Stores metadata in `MegaFileReference` table
- Fuzzy-matches filenames to songs in database

**What it doesn't do:**
- Download any files
- Mirror or redistribute content
- Scrape folder contents automatically

### Usage

Run manually via Discord admin command:

```
/jw admin reindex
```

This will:
1. Connect to each MEGA folder
2. Extract filename + download URL pairs
3. Match filenames to existing songs using fuzzy search
4. Store results in the database

### Download Link Exposure

MEGA links are similarly gated by `EXPOSE_MEGA_LINKS` environment flag:

- When `EXPOSE_MEGA_LINKS=false` (default): Indexed MEGA links are stored but never shown to users.
- When `EXPOSE_MEGA_LINKS=true`: MEGA download links are included when a user requests a song.

## Data Sync Strategy

### Initial Load

1. Use CSV/JSON import script to seed metadata
2. Run `/jw admin reindex` to index MEGA folders
3. Optionally fetch from Juiceboard API for verification

### Ongoing Updates

- Manual updates via `/jw admin add-song` or `/jw admin edit-song`
- Periodic MEGA reindex to catch new uploads
- Periodic Juiceboard API sync for official releases

### Conflict Resolution

If multiple sources have conflicting data:

1. Official Spotify/Apple Music data takes priority
2. Juice WRLD API data takes second priority
3. User-entered data and MEGA metadata are informational

## Safety Guarantees

The system ensures:

- ✅ No unauthorized file distribution
- ✅ Feature flags control download link exposure
- ✅ All URLs passed through `redact_private_urls()` before showing in public bot responses
- ✅ Admin-only commands for sensitive operations
- ✅ Audit logging for all admin actions

## Rate Limiting

Currently none. In production:

- Implement per-IP rate limiting on API endpoints
- Add caching (Redis) to reduce Juice WRLD API calls
- Consider request throttling for MEGA indexing
