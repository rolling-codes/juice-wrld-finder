"""Discord bot client setup."""
import logging
import asyncio
from discord.ext import commands
import discord

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JuiceWRLDBot(commands.Bot):
    """Juice WRLD metadata finder bot."""

    def __init__(self) -> None:
        """Initialize bot with intents."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix="/",
            intents=intents,
            help_command=None,
        )

    async def setup_hook(self) -> None:
        """Load cogs after bot connects."""
        try:
            await self.load_cog("app.bot.cogs.search_cog")
            logger.info("✓ Loaded search cog")
        except Exception as e:
            logger.error(f"Failed to load search cog: {e}")

        try:
            await self.load_cog("app.bot.cogs.admin_cog")
            logger.info("✓ Loaded admin cog")
        except Exception as e:
            logger.error(f"Failed to load admin cog: {e}")

    async def on_ready(self) -> None:
        """Called when bot is ready."""
        logger.info(f"✓ Bot ready! Logged in as {self.user}")

        # Sync commands with Discord
        try:
            synced = await self.tree.sync(guild=discord.Object(settings.discord_guild_id))
            logger.info(f"✓ Synced {len(synced)} command(s) with Discord")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")


bot = JuiceWRLDBot()


if __name__ == "__main__":
    asyncio.run(bot.start(settings.discord_token))
