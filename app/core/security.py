"""Security utilities for URL redaction and admin checks."""
import re
from typing import Any


def redact_private_urls(text: str) -> str:
    """Remove MEGA and other file-hosting URLs from text."""
    if not text:
        return text

    # Pattern to match MEGA URLs
    mega_pattern = r"https?://(?:mega\.nz|mega\.co\.nz)/[^\s]+"
    text = re.sub(mega_pattern, "[LINK REDACTED]", text, flags=re.IGNORECASE)

    # Pattern for other common file hosts
    file_hosts = r"https?://(?:gofile|catbox|vimeo|dropbox)[^\s]*"
    text = re.sub(file_hosts, "[LINK REDACTED]", text, flags=re.IGNORECASE)

    return text


async def check_admin_role(member: Any) -> bool:
    """Check if a Discord member has the admin role."""
    from app.core.config import settings

    if not hasattr(member, "roles"):
        return False

    role_ids = [role.id for role in member.roles]
    return settings.admin_role_id in role_ids
