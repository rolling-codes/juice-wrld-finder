"""Application configuration from environment variables."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App settings loaded from .env file."""

    # Discord
    discord_token: str
    discord_guild_id: int
    admin_role_id: int

    # Database
    database_url: str = "sqlite:///./juice_wrld.db"
    redis_url: str = "redis://localhost:6379"

    # API
    juicewrld_api_base: str = "https://juicewrldapi.com/api"

    # Feature flags
    expose_api_download_links: bool = False
    expose_mega_links: bool = False

    # MEGA links
    mega_main_comp: str = ""
    mega_era_comp: str = ""
    mega_cover_art_comp: str = ""
    mega_media_comp: str = ""
    mega_session_edits_comp: str = ""

    # Security
    secret_key: str
    admin_username: str = "admin"
    admin_password_hash: str = ""
    bot_api_key: str = ""

    # Web app
    cors_origins: list[str] = ["http://localhost:5173"]
    public_base_url: str = "http://localhost:8000"

    class Config:
        """Load from .env file."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
