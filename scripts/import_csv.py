"""CSV/JSON importer for bulk song loading."""
import csv
import json
import logging
from pathlib import Path

from app.db import SessionLocal
from app.models import DownloadLink
from app.repositories import SongRepository
from app.services import SongService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _split_pipes(value: str | None) -> list[str]:
    """Split pipe-delimited CSV cells while ignoring empty entries."""
    if not value:
        return []
    return [entry.strip() for entry in value.split("|") if entry.strip()]


def parse_versions(value: str | None) -> list[dict[str, object]]:
    """Parse a versions cell into repository-ready dictionaries.

    Supported pipe-delimited formats:
    - name
    - name:sort_order
    - name:base
    - name:sort_order:notes
    - name:base:notes
    """
    versions: list[dict[str, object]] = []
    for index, entry in enumerate(_split_pipes(value), start=1):
        parts = [part.strip() for part in entry.split(":", 2)]
        title = parts[0]
        if not title:
            continue

        sort_order = index
        is_base_version = False
        notes = None

        if len(parts) >= 2 and parts[1]:
            marker = parts[1].lower()
            if marker in {"base", "true", "yes", "1", "*"}:
                is_base_version = True
                sort_order = 0
            else:
                try:
                    sort_order = int(parts[1])
                except ValueError:
                    notes = parts[1]

        if len(parts) == 3 and parts[2]:
            notes = parts[2]

        versions.append(
            {
                "title": title,
                "is_base_version": is_base_version,
                "sort_order": sort_order,
                "notes": notes,
            }
        )
    return versions


def parse_references(value: str | None) -> list[dict[str, str | None]]:
    """Parse a references cell into repository-ready dictionaries.

    References are metadata citations, not download links. Use pipe-delimited
    entries with comma-separated fields: source_name,source_url,source_type,description.
    """
    references: list[dict[str, str | None]] = []
    for entry in _split_pipes(value):
        parts = [part.strip() for part in entry.split(",", 4)]
        if len(parts) == 1:
            source_name = parts[0]
            source_url = None
            source_type = "manual"
            description = None
        else:
            source_name = parts[0] or parts[1]
            source_url = parts[1] or None
            source_type = parts[2] if len(parts) > 2 and parts[2] else "manual"
            description = parts[3] if len(parts) > 3 and parts[3] else None

        if not source_name:
            continue

        references.append(
            {
                "source_name": source_name,
                "source_url": source_url,
                "source_type": source_type,
                "description": description,
            }
        )
    return references


def parse_download_links(value: str | None) -> list[dict[str, str]]:
    """Parse public/admin-approved download link entries.

    Use pipe-delimited entries with comma-separated fields:
    label,url,link_type,visibility.
    """
    links: list[dict[str, str]] = []
    for entry in _split_pipes(value):
        parts = [part.strip() for part in entry.split(",", 4)]
        if len(parts) < 2 or not parts[1]:
            continue

        links.append(
            {
                "label": parts[0] or "Download",
                "url": parts[1],
                "link_type": parts[2] if len(parts) > 2 and parts[2] else "other",
                "visibility": parts[3] if len(parts) > 3 and parts[3] else "bot",
            }
        )
    return links


def import_csv(filepath: str) -> None:
    """Import songs from CSV file."""
    db = SessionLocal()
    service = SongService(db)
    repo = SongRepository(db)

    try:
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                logger.error("CSV has no headers")
                return

            count = 0
            for row in reader:
                try:
                    song = service.create_song(
                        title=row.get("title", "").strip(),
                        era_name=row.get("era"),
                        release_status=row.get("release_status", "unknown"),
                        download_status=row.get("download_status", "metadata_only"),
                        official_url=row.get("official_url"),
                        api_download_url=row.get("api_download_url"),
                        notes=row.get("notes"),
                    )

                    # Add aliases
                    aliases = row.get("aliases", "")
                    if aliases:
                        for alias in aliases.split("|"):
                            service.add_alias(song.id, alias.strip())

                    # Add producers
                    producers = row.get("producers", "")
                    if producers:
                        for producer in producers.split("|"):
                            service.add_producer(song.id, producer.strip())

                    for version in parse_versions(row.get("versions")):
                        repo.add_version(song.id, **version)

                    for reference in parse_references(row.get("references")):
                        repo.add_reference(song.id, **reference)

                    for link in parse_download_links(row.get("download_links")):
                        db.add(DownloadLink(song_id=song.id, **link))
                    db.commit()

                    count += 1
                    if count % 10 == 0:
                        logger.info(f"Imported {count} songs...")

                except Exception as e:
                    logger.error(f"Error importing row {row.get('title')}: {e}")
                    continue

            logger.info(f"✓ Imported {count} songs from {filepath}")

    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
    except Exception as e:
        logger.error(f"Import error: {e}")
    finally:
        db.close()


def import_json(filepath: str) -> None:
    """Import songs from JSON file."""
    db = SessionLocal()
    service = SongService(db)
    repo = SongRepository(db)

    try:
        with open(filepath, encoding="utf-8") as f:
            songs_data = json.load(f)

        if not isinstance(songs_data, list):
            logger.error("JSON must be an array of song objects")
            return

        count = 0
        for song_data in songs_data:
            try:
                song = service.create_song(
                    title=song_data.get("title", ""),
                    era_name=song_data.get("era"),
                    release_status=song_data.get("release_status", "unknown"),
                    download_status=song_data.get("download_status", "metadata_only"),
                    official_url=song_data.get("official_url"),
                    api_download_url=song_data.get("api_download_url"),
                    notes=song_data.get("notes"),
                )

                # Add aliases
                for alias in song_data.get("aliases", []):
                    service.add_alias(song.id, alias)

                # Add producers
                for producer in song_data.get("producers", []):
                    service.add_producer(song.id, producer)

                for version in song_data.get("versions", []):
                    repo.add_version(
                        song.id,
                        title=version["title"],
                        version_type=version.get("version_type", "released"),
                        release_status=version.get("release_status", "unknown"),
                        is_base_version=version.get("is_base_version", False),
                        recorded_date=version.get("recorded_date"),
                        surfaced_date=version.get("surfaced_date"),
                        source_name=version.get("source_name"),
                        source_url=version.get("source_url"),
                        confidence=version.get("confidence", 1.0),
                        sort_order=version.get("sort_order", 0),
                        notes=version.get("notes"),
                    )

                for reference in song_data.get("references", []):
                    repo.add_reference(
                        song.id,
                        source_name=reference["source_name"],
                        source_type=reference.get("source_type", "manual"),
                        source_url=reference.get("source_url"),
                        description=reference.get("description"),
                        confidence=reference.get("confidence", 1.0),
                    )

                for link in song_data.get("download_links", []):
                    db.add(
                        DownloadLink(
                            song_id=song.id,
                            label=link.get("label", "Download"),
                            url=link.get("url", ""),
                            link_type=link.get("link_type", "other"),
                            visibility=link.get("visibility", "bot"),
                        )
                    )
                db.commit()

                count += 1
                if count % 10 == 0:
                    logger.info(f"Imported {count} songs...")

            except Exception as e:
                logger.error(f"Error importing song: {e}")
                continue

        logger.info(f"✓ Imported {count} songs from {filepath}")

    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
    except Exception as e:
        logger.error(f"Import error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python import_csv.py <filepath>")
        print("Supports .csv and .json files")
        sys.exit(1)

    filepath = sys.argv[1]
    ext = Path(filepath).suffix.lower()

    if ext == ".csv":
        import_csv(filepath)
    elif ext == ".json":
        import_json(filepath)
    else:
        print(f"Unsupported file type: {ext}")
        sys.exit(1)
