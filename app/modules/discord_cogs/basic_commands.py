import discord
from discord.ext import commands
from discord import app_commands
from typing import List, TypedDict
import logging

from tortoise.functions import Sum

from app.models import Clan, Player, Points, Season, Channel, GiftedSubsLeaderboard, Checkin, RaidCheckin

logger = logging.getLogger(__name__)

class Standings(TypedDict):
    name: str
    points: int
    tag: str

class PlayerStandings(TypedDict):
    name: str
    points: int
    clantag: str

class CheckinsStandings(TypedDict):
    name: str
    checkins: int

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
    
    @app_commands.command(name="standings", description="Get the current clan standings for the current season of the Battle of Midgard.")
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
    

    @app_commands.command(name="checkin-leaderboard", description="Get the checkin leaderboard for the twitch channel.")
    async def checkin_leaderboard(self, interaction: discord.Interaction) -> None:
        """
        /checkin-leaderboard command
        """
        
        # Each checkin is a separate row in the database, so we need to sum the checkins for each player.
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            standings: List[CheckinsStandings] = []

            for player in await Player.all().filter(channel=channel):
                no_of_checkins = await Checkin.all().filter(player=player).count()

                if no_of_checkins is not None:
                    player_standings: CheckinsStandings = {
                        "points": no_of_checkins,
                        "name": player.name,
                    }
                    standings.append(player_standings)
            
            sorted_standings = sorted(standings, key=lambda k: k["points"], reverse=True)

            embed = discord.Embed(title=f"Checkin Leaderboard:")
            embed.timestamp = interaction.created_at
            embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
            embed.color = discord.Color.green()

            position_list = ""
            names_list = ""
            checkins_list = ""

            count = 0
            for result in sorted_standings:
                count += 1
                position_list += f"{count}\n"
                names_list += f" {result['name'].title()}\n"
                checkins_list += f"{result['points']}\n"
                
            embed.add_field(name="Position", value=position_list, inline=True)
            embed.add_field(name="Player", value=names_list, inline=True)
            embed.add_field(name="Checkins", value=checkins_list, inline=True)
            
            await interaction.response.send_message(embed=embed)
        else:
            logger.info("This discord server has not been registered yet.")
            await interaction.response.send_message("This discord server has not been registered yet.")
    

    @app_commands.command(name="raid-checkin-leaderboard", description="Get the raid checkin leaderboard for the twitch channel.")
    async def raid_checkin_leaderboard(self, interaction: discord.Interaction) -> None:
        """
        /raid-checkin-leaderboard command
        """
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            standings: List[CheckinsStandings] = []

            for player in await Player.all().filter(channel=channel):
                no_of_checkins = await RaidCheckin.all().filter(player=player).count()

                if no_of_checkins is not None:
                    player_standings: CheckinsStandings = {
                        "points": no_of_checkins,
                        "name": player.name,
                    }
                    standings.append(player_standings)
            
            sorted_standings = sorted(standings, key=lambda k: k["points"], reverse=True)

            embed = discord.Embed(title=f"Raid Checkin Leaderboard:")
            embed.timestamp = interaction.created_at
            embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
            embed.color = discord.Color.green()

            position_list = ""
            names_list = ""
            checkins_list = ""

            count = 0
            for result in sorted_standings:
                count += 1
                position_list += f"{count}\n"
                names_list += f" {result['name'].title()}\n"
                checkins_list += f"{result['points']}\n"
                
            embed.add_field(name="Position", value=position_list, inline=True)
            embed.add_field(name="Player", value=names_list, inline=True)
            embed.add_field(name="Checkins", value=checkins_list, inline=True)
            
            await interaction.response.send_message(embed=embed)
        else:
            logger.info("This discord server has not been registered yet.")
            await interaction.response.send_message("This discord server has not been registered yet.")


    @app_commands.command(name="gifted-subs-leaderboard", description="Get the gifted subs leaderboard for the twitch channel.")
    async def gifted_subs_leaderboard(self, interaction: discord.Interaction) -> None:
        """
        /gifted-subs-leaderboard command
        """
        if await GiftedSubsLeaderboard.all().exists():
            leaderboard = await GiftedSubsLeaderboard.all()
            embed = discord.Embed(title="Gifted Subs Leaderboard:")
            embed.timestamp = interaction.created_at
            embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
            embed.color = discord.Color.green()

            position_list = ""
            names_list = ""
            gifted_subs_list = ""

            count = 0
            for result in leaderboard:
                player = await result.player.get()

                count += 1
                position_list += f"{count}\n"
                names_list += f" {player.name.title()}\n"
                gifted_subs_list += f"{result.gifted_subs}\n"
                
            embed.add_field(name="Position", value=position_list, inline=True)
            embed.add_field(name="Player", value=names_list, inline=True)
            embed.add_field(name="Gifted Subs", value=gifted_subs_list, inline=True)
            
            await interaction.response.send_message(embed=embed)
        else:
            logger.info("There are no entries in the gifted subs leaderboard.")
            await interaction.response.send_message("There are no entries in the gifted subs leaderboard.")
    

    @app_commands.command(name="lifetime-standings", description="Get the lifetime clan standings for the Battle of Midgard.")
    async def lifetime_standings(self, interaction: discord.Interaction) -> None:
        """
        /lifetime-standings command
        """
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            standings: List[Standings] = []
            for clan in await Clan.all().filter(channel=channel):
                clan_standings: Standings = {
                    "points": 0,
                    "name": clan.name,
                    "tag": clan.tag,
                }
                for points in await Points.filter(clan=clan, channel=channel):
                    clan_standings["points"] += points.points
                standings.append(clan_standings)
            sorted_standings = sorted(standings, key=lambda k: k["points"], reverse=True)

            embed = discord.Embed(title=f"Battle of Midgard Lifetime Clan Standings:")
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
            logger.info(f"This discord server ({interaction.guild.id}) has not been registered yet.")
            await interaction.response.send_message("This discord server has not been registered yet.")
    

    @app_commands.command(name="leaderboard", description="Get the individual leaderboard for the current season of the Battle of Midgard.")
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
                for result in sorted_standings[:100]:
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
    
    @app_commands.command(name="get-clan-player-counts", description="Get the player counts for each clan in the Battle of Midgard.")
    @commands.guild_only()
    async def get_clan_player_counts(self, interaction: discord.Interaction) -> None:
        """
        /get-clan-player-counts command
        """
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            clans = await Clan.all().filter(channel=channel)
            embed = discord.Embed(title=f"Battle of Midgard Clan Player Counts:")
            embed.timestamp = interaction.created_at
            embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
            embed.color = discord.Color.green()

            for clan in clans:
                player_count = await Player.all().filter(clan=clan).count()
                embed.add_field(name=f"{clan.name.title()}", value=f"{player_count} players", inline=True)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("This discord server has not been registered yet.")
    
    @app_commands.command(name="get-clan-players", description="Get the players for a specific clan in the Battle of Midgard.")
    @commands.guild_only()
    async def get_clan_players(self, interaction: discord.Interaction, clantag: str) -> None:
        """
        /get-clan-players command
        """
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            if await Clan.all().filter(channel=channel, tag=clantag).exists():
                clan = await Clan.get(channel=channel, tag=clantag)
                players = await Player.all().filter(clan=clan)
                embed = discord.Embed(title=f"Battle of Midgard Players in {clan.name.title()}:")
                embed.timestamp = interaction.created_at
                embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
                embed.color = discord.Color.green()

                names_list = ""

                for player in players:
                    names_list += f"{player.name.title()}\n"

                embed.add_field(name="Player", value=names_list, inline=True)

                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(f"Clan {clantag} does not exist.", ephemeral=True)
        else:
            await interaction.response.send_message("This discord server has not been registered yet.", ephemeral=True)
    
    @app_commands.command(name="check-player-clan", description="Check the clan of a specific player in the Battle of Midgard.")
    @commands.guild_only()
    async def check_player_clan(self, interaction: discord.Interaction, player_name: str) -> None:
        """
        /check-player-clan command
        """
        if await Channel.get_or_none(discord_server_id=interaction.guild.id):
            channel = await Channel.get(discord_server_id=interaction.guild.id)
            if await Player.all().filter(channel=channel, name=player_name).exists():
                player = await Player.get(channel=channel, name=player_name)
                clan = await player.clan.get()
                await interaction.response.send_message(f"{player.name} is in {clan.name} [{clan.tag}].")
            else:
                await interaction.response.send_message(f"Player {player_name} does not exist.", ephemeral=True)
        else:
            await interaction.response.send_message("This discord server has not been registered yet.", ephemeral=True)


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
            for result in sorted_standings[:100]:
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