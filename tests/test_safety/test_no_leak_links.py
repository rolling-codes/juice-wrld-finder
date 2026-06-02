"""Safety tests to verify no unauthorized links are leaked."""

from app.core.security import redact_private_urls


def test_redact_mega_links() -> None:
    """Test that MEGA links are redacted."""
    text = "Download from https://mega.nz/folder/ABCD1234#encrypted"
    redacted = redact_private_urls(text)

    assert "mega.nz" not in redacted
    assert "LINK REDACTED" in redacted


def test_redact_mega_co_nz() -> None:
    """Test that mega.co.nz links are redacted."""
    text = "Visit https://mega.co.nz/file/ABC#DEF"
    redacted = redact_private_urls(text)

    assert "mega" not in redacted


def test_redact_gofile_links() -> None:
    """Test that gofile links are redacted."""
    text = "Files at https://gofile.io/d/abc123"
    redacted = redact_private_urls(text)

    assert "gofile" not in redacted


def test_preserve_official_urls() -> None:
    """Test that official URLs are not redacted."""
    text = "Listen on https://open.spotify.com/track/123"
    redacted = redact_private_urls(text)

    assert "spotify.com" in redacted


def test_empty_string() -> None:
    """Test empty string handling."""
    result = redact_private_urls("")
    assert result == ""


def test_none_handling() -> None:
    """Test None handling."""
    result = redact_private_urls(None)
    assert result is None
