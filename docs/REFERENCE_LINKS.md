# Reference Links

These links are **for manual metadata verification only**. The bot and API do not automatically scrape, download, or distribute files from these sources.

## Important Note

This project is a **metadata search and discovery platform**, not a file distribution service. All download linking is strictly controlled via environment flags and is only used for:

- Official Juice WRLD releases (Spotify, Apple Music, YouTube)
- Juice WRLD API download links (when enabled)
- MEGA folder indexing for filename matching (when enabled)

## Manual Reference Folders

These MEGA folders contain Juice WRLD songs and are referenced for **metadata purposes only** (era, producers, aliases, track listings):

| Label | Link | Status |
|-------|------|--------|
| Main Comp | Configure with `MEGA_MAIN_COMP` | Optional |
| Era Comp | Configure with `MEGA_ERA_COMP` | Optional |
| Cover Art Comp | Configure with `MEGA_COVER_ART_COMP` | Optional |
| Media Comp | Configure with `MEGA_MEDIA_COMP` | Optional |
| Session Edits Comp | Configure with `MEGA_SESSION_EDITS_COMP` | Optional |

## Usage Policy

**Do not:**
- Automatically scrape these folders
- Download files programmatically
- Mirror or redistribute files
- Expose MEGA links in public bot responses (unless explicitly enabled by admin flag)
- Include copyrighted audio in the database

**Do:**
- Use these links manually to verify song metadata
- Index folder filenames for matching purposes
- Reference official release information
- Ask users to verify song details from official sources

## Version and Reference Records

The app stores references separately from download links. A reference can support metadata such as version type, earliest/base version, recorded date, surfaced date, source confidence, and notes. A reference URL is never used by `/downloads/{song_id}` unless an admin also creates a separate PUBLIC `DownloadLink`.

Supported reference labels include:

- Juice WRLD API
- Juice WRLD Vault
- Juicehub
- MusicBrainz
- Musicfetch
- SonoVault
- Manual

## Official Streaming Sources

For released songs, always link to official platforms:

- **Spotify:** [Juice WRLD on Spotify](https://open.spotify.com/artist/4MCBfE4596Uoi2O4DtmHO1)
- **Apple Music:** Juice WRLD Artist Profile
- **YouTube Music:** Juice WRLD Official Channel

## Juice WRLD API

The community Juice WRLD API at `https://juicewrldapi.com/` provides metadata and may include download links. This is used when `EXPOSE_API_DOWNLOAD_LINKS=true`.

- **API Base:** `https://juicewrldapi.com/api`
- **Docs:** `https://juicewrldapi.com/docs`
- **Status:** Community-maintained (unofficial, not endorsed by label)
