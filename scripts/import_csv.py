"""CSV/JSON importer for bulk song loading."""
import csv
import json
import logging
from pathlib import Path
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.services import SongService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def import_csv(filepath: str) -> None:
    """Import songs from CSV file."""
    db = SessionLocal()
    service = SongService(db)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
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

    try:
        with open(filepath, "r", encoding="utf-8") as f:
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
