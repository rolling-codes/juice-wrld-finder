"""Tests for CSV import parsing helpers."""
from scripts.import_csv import parse_download_links, parse_references, parse_versions


def test_parse_versions_supports_order_base_and_notes() -> None:
    """Version parser handles ordering, explicit base markers, and notes."""
    versions = parse_versions("Album Version:base|Studio Session:20:longer intro|Demo:10")

    assert versions == [
        {
            "title": "Album Version",
            "is_base_version": True,
            "sort_order": 0,
            "notes": None,
        },
        {
            "title": "Studio Session",
            "is_base_version": False,
            "sort_order": 20,
            "notes": "longer intro",
        },
        {
            "title": "Demo",
            "is_base_version": False,
            "sort_order": 10,
            "notes": None,
        },
    ]


def test_parse_references_supports_metadata_only_links() -> None:
    """Reference parser keeps source URLs as references, not downloads."""
    references = parse_references(
        "Genius,https://genius.com/example,lyrics,annotated lyrics|"
        "Interview,https://example.com/interview"
    )

    assert references == [
        {
            "source_name": "Genius",
            "source_url": "https://genius.com/example",
            "source_type": "lyrics",
            "description": "annotated lyrics",
        },
        {
            "source_name": "Interview",
            "source_url": "https://example.com/interview",
            "source_type": "manual",
            "description": None,
        },
    ]


def test_parse_download_links_supports_visibility() -> None:
    """Download parser keeps explicit labels, link types, and visibility."""
    links = parse_download_links(
        "Official,https://example.com/listen,official,public|"
        "Archive,https://example.com/archive,other,admin"
    )

    assert links == [
        {
            "label": "Official",
            "url": "https://example.com/listen",
            "link_type": "official",
            "visibility": "public",
        },
        {
            "label": "Archive",
            "url": "https://example.com/archive",
            "link_type": "other",
            "visibility": "admin",
        },
    ]
