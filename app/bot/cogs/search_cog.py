"""Search commands cog."""
import logging
from typing import Optional
import discord
from discord.ext import commands
from discord import app_commands

from app.core.security import redact_private_urls
from app.core.config import settings
from app.db import SessionLocal
from app.services import SearchService
from app.repositories import SongRepository

logger = logging.getLogger(__name__)


class SearchCog(commands.Cog):
    """Search-related commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize cog."""
        self.bot = bot

    @app_commands.command(name="search", description="Search for a song")
    @app_commands.describe(query="Song title, alias, or partial name")
    async def search(self, interaction: discord.Interaction, query: str) -> None:
        """Search for songs by title or alias."""
        await interaction.response.defer()

        db = SessionLocal()
        try:
            service = SearchService(db)
            results = service.search(query, limit=10)

            if not results:
                await interaction.followup.send(f"No songs found matching `{query}`")
                return

            embed = discord.Embed(
                title=f"Search Results for `{query}`",
                description=f"Found {len(results)} matching song(s)",
                color=discord.Color.green(),
            )

            for result in results:
                song = result.song
                confidence = f"{result.confidence:.0f}%"
                title = f"{song.title} (confidence: {confidence})"
                embed.add_field(
                    name=title,
                    value=f"Status: {song.release_status} | ID: {song.id}",
                    inline=False,
                )

            embed = self._redact_embed(embed)
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logger.error(f"Search error: {e}")
            await interaction.followup.send("Search failed, please try again later")
        finally:
            db.close()

    @app_commands.command(name="song", description="Get full song details")
    @app_commands.describe(song_id="Song ID number")
    async def song(self, interaction: discord.Interaction, song_id: int) -> None:
        """Get detailed info about a song."""
        await interaction.response.defer()

        db = SessionLocal()
        try:
            repo = SongRepository(db)
            song = repo.get_by_id(song_id)

            if not song:
                await interaction.followup.send(f"Song with ID {song_id} not found")
                return

            embed = discord.Embed(
                title=song.title,
                color=discord.Color.blue(),
            )

            embed.add_field(name="Status", value=song.release_status, inline=True)
            embed.add_field(name="Download Status", value=song.download_status, inline=True)

            if song.era:
                embed.add_field(name="Era", value=song.era.name, inline=True)

            if song.official_url:
                embed.add_field(
                    name="Official Link",
                    value=f"[Listen]({song.official_url})",
                    inline=False,
                )

            if song.api_download_url and settings.expose_api_download_links:
                embed.add_field(
                    name="Download",
                    value=f"[Available]({song.api_download_url})",
                    inline=False,
                )

            if song.notes:
                notes = redact_private_urls(song.notes)
                embed.add_field(name="Notes", value=notes, inline=False)

            if song.aliases:
                alias_list = ", ".join([a.alias for a in song.aliases])
                embed.add_field(name="Aliases", value=alias_list, inline=False)

            embed = self._redact_embed(embed)
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logger.error(f"Song fetch error: {e}")
            await interaction.followup.send("Failed to fetch song details")
        finally:
            db.close()

    @app_commands.command(name="era", description="Get songs from an era")
    @app_commands.describe(era_name="Era name")
    async def era(self, interaction: discord.Interaction, era_name: str) -> None:
        """Search songs from a specific era."""
        await interaction.response.defer()

        db = SessionLocal()
        try:
            era = db.query(Era).filter(Era.name.ilike(f"%{era_name}%")).first()

            if not era:
                await interaction.followup.send(f"Era `{era_name}` not found")
                return

            repo = SongRepository(db)
            songs = repo.get_by_era_id(era.id, limit=20)

            if not songs:
                await interaction.followup.send(f"No songs found in era `{era.name}`")
                return

            embed = discord.Embed(
                title=f"Songs from {era.name} Era",
                description=f"Found {len(songs)} song(s)",
                color=discord.Color.purple(),
            )

            for song in songs:
                embed.add_field(
                    name=song.title,
                    value=f"{song.release_status}",
                    inline=True,
                )

            embed = self._redact_embed(embed)
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logger.error(f"Era search error: {e}")
            await interaction.followup.send("Era search failed")
        finally:
            db.close()

    @app_commands.command(name="random", description="Get a random song")
    async def random(self, interaction: discord.Interaction) -> None:
        """Get a random song."""
        await interaction.response.defer()

        db = SessionLocal()
        try:
            service = SearchService(db)
            song = service.get_random_song()

            if not song:
                await interaction.followup.send("No songs in database")
                return

            embed = discord.Embed(
                title=f"🎲 Random Song: {song.title}",
                color=discord.Color.gold(),
            )

            embed.add_field(name="Status", value=song.release_status, inline=True)
            embed.add_field(name="Download", value=song.download_status, inline=True)

            embed = self._redact_embed(embed)
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logger.error(f"Random song error: {e}")
            await interaction.followup.send("Failed to get random song")
        finally:
            db.close()

    def _redact_embed(self, embed: discord.Embed) -> discord.Embed:
        """Redact private URLs from embed."""
        if embed.title:
            embed.title = redact_private_urls(embed.title)
        if embed.description:
            embed.description = redact_private_urls(embed.description)

        for i, field in enumerate(embed.fields):
            embed.set_field_at(
                i,
                name=redact_private_urls(field.name),
                value=redact_private_urls(field.value),
                inline=field.inline,
            )

        return embed


async def setup(bot: commands.Bot) -> None:
    """Setup cog."""
    await bot.add_cog(SearchCog(bot))


from app.models import Era
