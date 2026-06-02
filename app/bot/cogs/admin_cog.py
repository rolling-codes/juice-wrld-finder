"""Admin commands cog."""
import logging
import discord
from discord.ext import commands
from discord import app_commands

from app.core.config import settings
from app.core.security import check_admin_role
from app.db import SessionLocal
from app.services import SongService
from app.integrations import MEGAIndexer

logger = logging.getLogger(__name__)


class AdminCog(commands.Cog):
    """Admin-only commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize cog."""
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> bool:
        """Check if user has admin role."""
        if not hasattr(ctx.author, "roles"):
            return False
        role_ids = [role.id for role in ctx.author.roles]
        return settings.admin_role_id in role_ids

    @app_commands.command(name="add-song", description="Add a new song (Admin only)")
    @app_commands.describe(
        title="Song title",
        era="Era name (optional)",
        release_status="released/unreleased (default: unknown)",
    )
    async def add_song(
        self,
        interaction: discord.Interaction,
        title: str,
        era: str = None,
        release_status: str = "unknown",
    ) -> None:
        """Add a new song to the database."""
        if not await check_admin_role(interaction.user):
            await interaction.response.send_message("Admin only", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        db = SessionLocal()
        try:
            service = SongService(db)
            song = service.create_song(
                title=title,
                era_name=era,
                release_status=release_status,
            )

            await interaction.followup.send(
                f"✓ Created song: {song.title} (ID: {song.id})",
                ephemeral=True,
            )

        except Exception as e:
            logger.error(f"Error adding song: {e}")
            await interaction.followup.send(
                f"Failed to add song: {e}",
                ephemeral=True,
            )
        finally:
            db.close()

    @app_commands.command(name="reindex", description="Reindex MEGA folders (Admin only)")
    async def reindex(self, interaction: discord.Interaction) -> None:
        """Reindex MEGA folder contents."""
        if not await check_admin_role(interaction.user):
            await interaction.response.send_message("Admin only", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        db = SessionLocal()
        try:
            indexer = MEGAIndexer(db)
            stats = indexer.index_folders()

            await interaction.followup.send(
                f"✓ Reindex complete\n"
                f"Indexed: {stats['indexed']} files\n"
                f"Matched: {stats['matched']} songs\n"
                f"Errors: {stats['errors']}",
                ephemeral=True,
            )

        except Exception as e:
            logger.error(f"Reindex error: {e}")
            await interaction.followup.send(
                f"Reindex failed: {e}",
                ephemeral=True,
            )
        finally:
            db.close()


async def setup(bot: commands.Bot) -> None:
    """Setup cog."""
    await bot.add_cog(AdminCog(bot))
