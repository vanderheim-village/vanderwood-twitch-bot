import discord
from discord.ext import commands
from discord import app_commands
from typing import List, TypedDict
import logging

from tortoise.functions import Sum

from app.models import Checkin, Clan, Player, Points, Season, Session, Channel

logger = logging.getLogger(__name__)

class Standings(TypedDict):
    name: str
    points: int
    tag: str

class PlayerStandings(TypedDict):
    name: str
    points: int
    clantag: str

class BasicCommandsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="help", description="Get a list of commands which this bot supports.")
    async def help(self, interaction: discord.Interaction) -> None:
        """
        /help command
        """
        await interaction.response.send_message(
            f"You can view the list of commands which this bot supports here: {self.bot.conf_options['APP']['BOT_COMMANDS_LINK']}."
        )
    
    @app_commands.command(name="standings", description="Get the current standings for the current season.")
    async def standings(self, interaction: discord.Interaction) -> None:
        """
        /standings command
        """
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                season = await Season.active_seasons.all().filter(channel=channel).first()
                standings: List[Standings] = []
                for clan in await Clan.all().filter(channel=channel):
                    clan_standings: Standings = {
                        "points": 0,
                        "name": clan.name,
                        "tag": clan.tag,
                    }
                    for points in await Points.filter(season=season, clan=clan, channel=channel):
                        clan_standings["points"] += points.points
                    standings.append(clan_standings)
                sorted_standings = sorted(standings, key=lambda k: k["points"], reverse=True)

                embed = discord.Embed(title=f"Battle of Midgard Clan Standings | {season.name}:")
                embed.timestamp = interaction.created_at
                embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
                embed.color = discord.Color.green()

                position_list = ""
                names_list = ""
                points_list = ""

                count = 0
                for result in sorted_standings:
                    count += 1
                    position_list += f"{count}\n"
                    names_list += f" {result['name'].title()}\n"
                    points_list += f"{result['points']}\n"
                    
                embed.add_field(name="Position", value=position_list, inline=True)
                embed.add_field(name="Clan", value=names_list, inline=True)
                embed.add_field(name="Points", value=points_list, inline=True)
                
                await interaction.response.send_message(embed=embed)
            else:
                logger.info(f"There are no active seasons for this discord server ({interaction.guild.id}).")
                await interaction.response.send_message("There are no active seasons.")
        else:
            logger.info(f"This discord server ({interaction.guild.id}) has not been registered yet.")
            await interaction.response.send_message("This discord server has not been registered yet.")
    

    @app_commands.command(name="leaderboard", description="Get the current individual leaderboard for the current season.")
    async def leaderboard(self, interaction: discord.Interaction) -> None:
        """
        /leaderboard command
        """
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                season = await Season.active_seasons.all().filter(channel=channel).first()
                standings: List[PlayerStandings] = []
                for points_row in await Points.filter(season=season, channel=channel):
                    player = await points_row.player.get()
                    assert player.clan is not None
                    player_standings: PlayerStandings = {
                        "points": points_row.points,
                        "name": player.name,
                        "clantag": (await player.clan.get()).tag,
                    }
                    standings.append(player_standings)
                sorted_standings = sorted(standings, key=lambda k: k["points"], reverse=True)

                embed = discord.Embed(title=f"Battle of Midgard Individual Leaderboard | {season.name}:")
                embed.timestamp = interaction.created_at
                embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
                embed.color = discord.Color.green()

                position_list = ""
                names_list = ""
                points_list = ""

                count = 0
                for result in sorted_standings[:10]:
                    count += 1
                    position_list += f"{count}\n"
                    names_list += f" {result['name'].title()}\n"
                    points_list += f"{result['points']}\n"
                
                embed.add_field(name="Position", value=position_list, inline=True)
                embed.add_field(name="Player", value=names_list, inline=True)
                embed.add_field(name="Points", value=points_list, inline=True)

                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("There are no active seasons.")
        else:
            await interaction.response.send_message("This discord server has not been registered yet.")


    @app_commands.command(name="lifetime-leaderboard", description="Get the lifetime individual leaderboard for the Battle of Midgard.")
    async def lifetime_leaderboard(self, interaction: discord.Interaction) -> None:
        """
        /lifetime-leaderboard command
        """
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            standings: List[PlayerStandings] = []
            
            ## Get all the points for each player, each player can have multiple rows for each season. These need summing together. We can use .annotate(sum=Sum("points")).values_list("sum"))[0]

            for player in await Player.all():
                lifetime_points = (
                    await Points.get(player=player, channel=channel)
                    .annotate(sum=Sum("points"))
                    .values_list("sum")
                )[0]

                if lifetime_points is not None:
                    player_standings: PlayerStandings = {
                        "points": lifetime_points,
                        "name": player.name,
                        "clantag": (await player.clan.get()).tag,
                    }
                    standings.append(player_standings)
            
            sorted_standings = sorted(standings, key=lambda k: k["points"], reverse=True)

            embed = discord.Embed(title=f"Battle of Midgard Lifetime Individual Leaderboard:")
            embed.timestamp = interaction.created_at
            embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
            embed.color = discord.Color.green()

            position_list = ""
            names_list = ""
            points_list = ""

            count = 0
            for result in sorted_standings[:10]:
                count += 1
                position_list += f"{count}\n"
                names_list += f" {result['name'].title()}\n"
                points_list += f"{result['points']}\n"
                
            embed.add_field(name="Position", value=position_list, inline=True)
            embed.add_field(name="Player", value=names_list, inline=True)
            embed.add_field(name="Points", value=points_list, inline=True)

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("This discord server has not been registered yet.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BasicCommandsCog(bot))