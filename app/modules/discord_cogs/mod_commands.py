import logging
import random
from typing import TYPE_CHECKING, Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands
from tortoise import timezone
from tortoise.functions import Count
from twitchio.ext import commands as twitch_commands

from app.models import Channel, Checkin, Clan, Player, Points, Season, Session

if TYPE_CHECKING:
    from bot import DiscordBot, TwitchBot

logger = logging.getLogger(__name__)


class ModCommandsCog(commands.Cog):
    def __init__(self, bot: "DiscordBot", twitch_bot: "TwitchBot") -> None:
        self.twitch_bot = twitch_bot
        self.bot = bot

    @app_commands.command(
        name="get-auth-link", description="Get the authorization link for the twitch bot."
    )
    @commands.guild_only()
    @commands.has_any_role("Moderator", "Admin", "Admins", "Moderators")
    async def get_auth_link(self, interaction: discord.Interaction) -> None:
        """
        Provides the OAuth link for the user to authorize the app with all scopes.
        """
        all_scopes = [
            "analytics:read:extensions",
            "analytics:read:games",
            "bits:read",
            "channel:edit:commercial",
            "channel:manage:broadcast",
            "channel:manage:moderators",
            "channel:manage:polls",
            "channel:manage:predictions",
            "channel:manage:redemptions",
            "channel:manage:schedule",
            "channel:manage:videos",
            "channel:read:editors",
            "channel:read:goals",
            "channel:read:hype_train",
            "channel:read:polls",
            "channel:read:predictions",
            "channel:read:redemptions",
            "channel:read:stream_key",
            "channel:read:subscriptions",
            "clips:edit",
            "moderation:read",
            "moderator:manage:announcements",
            "moderator:manage:automod",
            "moderator:manage:banned_users",
            "moderator:manage:chat_messages",
            "moderator:manage:chat_settings",
            "moderator:manage:shoutouts",
            "moderator:read:automod_settings",
            "moderator:read:blocked_terms",
            "moderator:read:chat_settings",
            "user:edit",
            "user:edit:follows",
            "user:manage:blocked_users",
            "user:read:blocked_users",
            "user:read:broadcast",
            "user:read:email",
            "user:read:follows",
            "user:read:subscriptions",
        ]

        callback_url = self.twitch_bot.conf_options["APP"]["CALLBACK_URL"]

        # URL encode the scopes into one string
        encoded_scopes = "%20".join(all_scopes)

        auth_url = (
            "https://id.twitch.tv/oauth2/authorize"
            f"?client_id={self.twitch_bot.client_id}"
            f"&redirect_uri={callback_url}"
            f"&response_type=code"
            f"&scope={encoded_scopes}"
        )

        await interaction.response.send_message(auth_url, ephemeral=True)

    @app_commands.command(
        name="set-nickname",
        description="Set a players nickname, used for triggerfyre if name too long.",
    )
    @commands.guild_only()
    @commands.has_any_role("Moderator", "Admin", "Admins", "Moderators")
    async def set_nickname(
        self, interaction: discord.Interaction, player: str, nickname: str
    ) -> None:
        """
        /set-nickname <player> <nickname>
        """
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            if await Player.get_or_none(name=player, channel=channel):
                player_obj = await Player.get(name=player, channel=channel)
                player_obj.nickname = nickname
                await player_obj.save()

                await interaction.response.send_message(
                    f"Added the nickname {nickname} to the player {player}."
                )
            else:
                await interaction.response.send_message(f"The player {player} doesn't exist.")
        else:
            await interaction.response.send_message(
                f"This discord server is not registered.", ephemeral=True
            )

    @app_commands.command(
        name="add-points",
        description="Add points to a player for the current season of the Battle of Midgard.",
    )
    @commands.guild_only()
    @commands.has_any_role("Moderator", "Admin", "Admins", "Moderators")
    async def add_points(self, interaction: discord.Interaction, player: str, points: int) -> None:
        """
        /add-points <player> <points>
        """
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                season = await Season.active_seasons.all().filter(channel=channel).first()
                if await Player.get_or_none(name=player, channel=channel):
                    player = await Player.get(name=player, channel=channel)
                    if player.is_enabled() and player.clan:
                        clan = await player.clan.get()
                        if await Points.get_or_none(player=player, season=season, channel=channel):
                            points_obj = await Points.get(
                                player=player, season=season, channel=channel
                            )
                            points_obj.points += points
                            await points_obj.save()
                            await interaction.response.send_message(
                                f"Added {points} points to {player.name}.", ephemeral=True
                            )
                        else:
                            await Points.create(
                                player=player,
                                season=season,
                                channel=channel,
                                points=points,
                                clan_id=clan.id,
                            )
                            await interaction.response.send_message(
                                f"Added {points} points to {player.name}.", ephemeral=True
                            )
                    else:
                        await interaction.response.send_message(
                            f"Player {player.name} is not enabled or has no clan.", ephemeral=True
                        )
                else:
                    await interaction.response.send_message(
                        f"Player {player} not found.", ephemeral=True
                    )
            else:
                await interaction.response.send_message(f"No active season found.", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"This discord server is not registered.", ephemeral=True
            )

    @app_commands.command(
        name="remove-points",
        description="Remove points from a player for the current season of the Battle of Midgard.",
    )
    @commands.guild_only()
    @commands.has_any_role("Moderator", "Admin", "Admins", "Moderators")
    async def remove_points(
        self, interaction: discord.Interaction, player: str, points: int
    ) -> None:
        """
        /remove-points <player> <points>
        """
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                season = await Season.active_seasons.all().filter(channel=channel).first()
                if await Player.all().filter(name=player).exists():
                    player_object = await Player.all().filter(name=player, channel=channel).first()
                    if (
                        await Points.all()
                        .filter(player=player_object, season=season, channel=channel)
                        .exists()
                    ):
                        points_obj = (
                            await Points.all()
                            .filter(player=player_object, season=season, channel=channel)
                            .first()
                        )
                        points_obj.points -= points
                        await points_obj.save()
                        await interaction.response.send_message(
                            f"Removed {points} points from {player}.", ephemeral=True
                        )
                    else:
                        await interaction.response.send_message(
                            f"The player {player} has no points.", ephemeral=True
                        )
                else:
                    await interaction.response.send_message(
                        f"Player {player} not found.", ephemeral=True
                    )
            else:
                await interaction.response.send_message(f"No active season found.", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"This discord server is not registered.", ephemeral=True
            )

    @app_commands.command(
        name="start-season", description="Start a new season of the Battle of Midgard."
    )
    @commands.guild_only()
    @commands.has_any_role("Moderator", "Admin", "Admins", "Moderators")
    async def start_season(self, interaction: discord.Interaction, season_name: str) -> None:
        """
        /start-season <season_name>
        """
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                await interaction.response.send_message(
                    f"There is already an active season.", ephemeral=True
                )
            else:
                await Season.create(name=season_name, channel=channel)
                await interaction.response.send_message(
                    f"Started season {season_name}.", ephemeral=True
                )
        else:
            await interaction.response.send_message(
                f"This discord server is not registered.", ephemeral=True
            )

    @app_commands.command(
        name="end-season", description="End the current season of the Battle of Midgard."
    )
    @commands.guild_only()
    @commands.has_any_role("Moderator", "Admin", "Admins", "Moderators")
    async def end_season(self, interaction: discord.Interaction) -> None:
        """
        /end-season
        """
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                if await Session.active_session.all().filter(channel=channel).exists():
                    await interaction.response.send_message(
                        f"There is an active session. Please end the session first.", ephemeral=True
                    )
                else:
                    active_season = (
                        await Season.active_seasons.all().filter(channel=channel).first()
                    )
                    await Season.active_seasons.all().filter(channel=channel).update(
                        end_date=timezone.now()
                    )
                    await interaction.response.send_message(
                        f"Ended season {active_season.name}.", ephemeral=True
                    )
            else:
                await interaction.response.send_message(
                    f"There is no active season.", ephemeral=True
                )
        else:
            await interaction.response.send_message(
                f"This discord server is not registered.", ephemeral=True
            )

    @app_commands.command(
        name="start-session", description="Start a new session of the Battle of Midgard."
    )
    @commands.guild_only()
    @commands.has_any_role("Moderator", "Admin", "Admins", "Moderators")
    async def start_session(self, interaction: discord.Interaction) -> None:
        """
        /start-session
        """
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                if await Session.active_session.all().filter(channel=channel).exists():
                    await interaction.response.send_message(
                        f"There is already an active session.", ephemeral=True
                    )
                else:
                    active_season = (
                        await Season.active_seasons.all().filter(channel=channel).first()
                    )
                    await Session.create(season=active_season, channel=channel)
                    await interaction.response.send_message(
                        f"Started a new session of the Battle of Midgard.", ephemeral=True
                    )
            else:
                await interaction.response.send_message(
                    f"There is no active season.", ephemeral=True
                )
        else:
            await interaction.response.send_message(
                f"This discord server is not registered.", ephemeral=True
            )

    @app_commands.command(
        name="end-session", description="End the current session of the Battle of Midgard."
    )
    @commands.guild_only()
    @commands.has_any_role("Moderator", "Admin", "Admins", "Moderators")
    async def end_session(self, interaction: discord.Interaction) -> None:
        """
        /end-session
        """
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                if await Session.active_session.all().filter(channel=channel).exists():
                    await Session.active_session.all().filter(channel=channel).update(
                        end_time=timezone.now()
                    )
                    await interaction.response.send_message(
                        f"Ended the current session of the Battle of Midgard.", ephemeral=True
                    )
                else:
                    await interaction.response.send_message(
                        f"There is no active session.", ephemeral=True
                    )
            else:
                await interaction.response.send_message(
                    f"There is no active season.", ephemeral=True
                )
        else:
            await interaction.response.send_message(
                f"This discord server is not registered.", ephemeral=True
            )

    @app_commands.command(name="add-player", description="Add a player to the Battle of Midgard.")
    @commands.guild_only()
    @commands.has_any_role("Moderator", "Admin", "Admins", "Moderators")
    async def add_player(self, interaction: discord.Interaction, player_name: str) -> None:
        """
        /add-player <player_name> <clan>
        """
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            if await Player.all().filter(name=player_name, channel=channel).exists():
                await interaction.response.send_message(
                    f"Player {player_name} already exists.", ephemeral=True
                )
            else:
                clan_totals = (
                    await Clan.all()
                    .filter(channel=channel)
                    .annotate(count=Count("players", distinct=True))
                    .values("id", "name", "tag", "count")
                )
                min_total = min(clan_totals, key=lambda x: x["count"])
                clans_to_choose_from = [
                    clan["id"] for clan in clan_totals if clan["count"] == min_total["count"]
                ]
                new_clan = random.choice(clans_to_choose_from)
                await Player.create(name=player_name.lower(), clan_id=new_clan, channel=channel)
                logging.info(f"Created player {player_name.lower()}.")
                await interaction.response.send_message(
                    f"Player {player_name} added to the Battle of Midgard.", ephemeral=True
                )
        else:
            await interaction.response.send_message(
                f"This discord server is not registered.", ephemeral=True
            )

    @app_commands.command(
        name="fix-missing-sub-points",
        description="Fix missing sub points for the current season of the Battle of Midgard.",
    )
    @commands.guild_only()
    @commands.has_any_role("Moderator", "Admin", "Admins", "Moderators")
    async def fix_missing_sub_points(self, interaction: discord.Interaction) -> None:
        """
        /fix-missing-sub-points

        If player has no lifetime points then add 1000 points for the current season.
        """
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                season = await Season.active_seasons.all().filter(channel=channel).first()
                players = await Player.all().filter(channel=channel)
                for player in players:
                    if not await Points.all().filter(player=player, channel=channel).exists():
                        clan = await player.clan.get()
                        await Points.create(
                            player=player, season=season, channel=channel, clan=clan, points=1000
                        )
                        logging.info(f"Added 1000 points to {player.name}.")
                    else:
                        if (
                            await Points.all()
                            .filter(player=player, season=season, channel=channel)
                            .exists()
                        ):
                            points = (
                                await Points.all()
                                .filter(player=player, season=season, channel=channel)
                                .first()
                            )
                            if points.points == 0:
                                points.points = 1000
                                await points.save()
                                logging.info(f"Added 1000 points to {player.name}.")
                await interaction.response.send_message(
                    f"Fixed missing sub points.", ephemeral=True
                )


async def setup(bot: commands.Bot, twitch_bot: twitch_commands.Bot) -> None:
    await bot.add_cog(ModCommandsCog(bot, twitch_bot))
