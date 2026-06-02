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
| Main Comp | [Main Compilation](https://mega.nz/folder/LU9gWY7Z#PMTqIPB69dT0OW5CiHEizQ) | Active |
| Era Comp | [Era Compilation](https://mega.nz/folder/XREQ3A7a#1IYPO9liju-ORDSZs4JJCQ) | Outdated |
| Cover Art Comp | [Cover Art](https://mega.nz/folder/6B5wmJzL#OeN-JJXayEHfXyLYhLfBkg) | Active |
| Media Comp | [Media References](https://mega.nz/folder/XU5FUCxJ#gECLcpANW9MkVFZtCfMe3Q) | Active |
| Session Edits Comp | [Session Edits](https://mega.nz/folder/DYZWiBBD#dtXjRHEOJTi2KWYGR2MGew) | Active |

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

## Official Streaming Sources

For released songs, always link to official platforms:

- **Spotify:** [Juice WRLD on Spotify](https://open.spotify.com/artist/4MCBfE4596Uoi2O4DtmHO1)
- **Apple Music:** Juice WRLD Artist Profile
- **YouTube Music:** Juice WRLD Official Channel

## Juice WRLD API

The community Juice WRLD API at `https://juicewrldapi.com/` provides metadata and may include download links. This is used when `EXPOSE_API_DOWNLOAD_LINKS=true`.

- **API Base:** https://juicewrldapi.com/api
- **Docs:** https://juicewrldapi.com/docs
- **Status:** Community-maintained (unofficial, not endorsed by label)
