from typing import List, TypedDict, TYPE_CHECKING
from datetime import datetime, timedelta, timezone

from tortoise.functions import Sum
from twitchio.ext import commands
from discord.ext import commands as discord_commands

from app.models import Checkin, Clan, Player, Points, Season, Session, Channel, RaidSession, RaidCheckin, GiftedSubsLeaderboard, FollowerGiveaway, FollowerGiveawayEntry, SpoilsSession, SpoilsClaim

if TYPE_CHECKING:
    from bot import TwitchBot, DiscordBot

class Standings(TypedDict):
    name: str
    points: int
    tag: str


class PlayerStandings(TypedDict):
    name: str
    points: int
    clantag: str


class GiftedSubsLeaderboardStandings(TypedDict):
    name: str
    gifted_subs: int


class BomCommandsCog(commands.Cog):
    def __init__(self, twitch_bot: "TwitchBot", discord_bot: "DiscordBot") -> None:
        self.twitch_bot = twitch_bot
        self.discord_bot = discord_bot

    
    @commands.command()
    async def giftedsubleaderboard(self, ctx: commands.Context) -> None:
        """
        ?giftsubleaderboard command

        Display the top 10 leaderboard for gifted subs.
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            leaderboard: List[GiftedSubsLeaderboard] = []
            for player_row in await GiftedSubsLeaderboard.filter(channel=channel):
                player_object = await player_row.player.get()
                leaderboard_entry: GiftedSubsLeaderboardStandings = {
                    "name": player_object.name,
                    "gifted_subs": player_row.gifted_subs,
                }
                leaderboard.append(leaderboard_entry)
            sorted_leaderboard = sorted(leaderboard, key=lambda k: k["gifted_subs"], reverse=True)
            await ctx.send(f"BOM | Gifted Subs Leaderboard:")
            count = 0
            for result in sorted_leaderboard[:10]:
                count += 1
                await ctx.send(f"{count}. {result['name']} - {result['gifted_subs']}")
        else:
            pass

    @commands.command()
    async def rank(self, ctx: commands.Context, clanname: str) -> None:
        """
        ?rank command

        Display the top 10 players in the clan for the current season.
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                season = await Season.active_seasons.all().filter(channel=channel).first()
                if await Clan.get_or_none(tag=clanname, channel=channel):
                    clan = await Clan.get(tag=clanname, channel=channel)
                    standings: List[PlayerStandings] = []
                    for points_row in await Points.filter(season=season, clan=clan, channel=channel):
                        player = await points_row.player.get()
                        player_standings: PlayerStandings = {
                            "points": points_row.points,
                            "name": player.name,
                            "clantag": clan.tag,
                        }
                        standings.append(player_standings)
                    sorted_standings = sorted(standings, key=lambda k: k["points"], reverse=True)
                    await ctx.send(f"BOM | {season.name}:")
                    count = 0
                    for result in sorted_standings[:10]:
                        count += 1
                        await ctx.send(
                            f"{count}. [{result['clantag']}] {result['name']} - {result['points']}"
                        )
                else:
                    await ctx.send(f"Clan {clanname} does not exist.")
            else:
                await ctx.send("No active season.")
        else:
            pass

    @commands.command()
    async def standings(self, ctx: commands.Context) -> None:
        """
        ?standings command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
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
                await ctx.send(f"BOM | {season.name}:")
                count = 0
                for result in sorted_standings:
                    count += 1
                    await ctx.send(f"{count}. [{result['tag']}] {result['name']} - {result['points']}")
            else:
                await ctx.send("No active seasons!")
        else:
            pass

    @commands.command()
    async def overallrank(self, ctx: commands.Context) -> None:
        """
        ?overallrank command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
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
                await ctx.send(f"BOM | {season.name}:")
                count = 0
                for result in sorted_standings[:10]:
                    count += 1
                    await ctx.send(
                        f"{count}. [{result['clantag']}] {result['name']} - {result['points']}"
                    )
            else:
                await ctx.send("No active seasons!")
        else:
            pass

    @commands.command()
    async def myrank(self, ctx: commands.Context) -> None:
        """
        ?myrank command

        Display current season points, lifetime points, current season rank in clan and overall rank for current season.
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                if await Player.get_or_none(name=ctx.author.name.lower(), channel=channel):
                    player = await Player.get(name=ctx.author.name.lower(), channel=channel)
                    active_season = await Season.active_seasons.all().filter(channel=channel).first()
                    assert player.clan is not None
                    if await player.clan.get() is None:
                        await ctx.send("You are not in a clan.")
                    else:
                        clan = await player.clan.get()
                        if await Points.get_or_none(player=player, season=active_season, channel=channel):
                            current_season_points = (
                                await Points.get(player=player, season=active_season, channel=channel)
                            ).points
                        else:
                            current_season_points = 0
                        if await Player.get_or_none(name=player.name, channel=channel):
                            lifetime_points = (
                                await Points.get(player=player, channel=channel)
                                .annotate(sum=Sum("points"))
                                .values_list("sum")
                            )[0]
                            print(lifetime_points)
                        else:
                            lifetime_points = 0

                        if await Points.get_or_none(player=player, season=active_season, channel=channel):
                            standings: List[PlayerStandings] = []
                            for points_row in await Points.filter(season=active_season, channel=channel):
                                player = await points_row.player.get()
                                assert player.clan is not None
                                player_standings: PlayerStandings = {
                                    "points": points_row.points,
                                    "name": player.name,
                                    "clantag": (await player.clan.get()).tag,
                                }
                                standings.append(player_standings)
                            sorted_standings = sorted(
                                standings, key=lambda k: k["points"], reverse=True
                            )
                            count = 0
                            for result in sorted_standings:
                                count += 1
                                if result["name"] == ctx.author.name.lower():
                                    current_season_overall_rank = count
                                    break
                        else:
                            current_season_overall_rank = 0

                        if await Points.get_or_none(player=player, season=active_season, channel=channel):
                            clan_standings: List[PlayerStandings] = []
                            for points_row in await Points.filter(season=active_season, clan=clan, channel=channel):
                                player = await points_row.player.get()
                                assert player.clan is not None
                                clan_player_standings: PlayerStandings = {
                                    "points": points_row.points,
                                    "name": player.name,
                                    "clantag": (await player.clan.get()).tag,
                                }
                                clan_standings.append(clan_player_standings)
                            clan_sorted_standings = sorted(
                                clan_standings, key=lambda k: k["points"], reverse=True
                            )
                            count = 0
                            for result in clan_sorted_standings:
                                count += 1
                                if result["name"] == ctx.author.name.lower():
                                    current_season_clan_rank = count
                                    break
                        else:
                            current_season_clan_rank = 0

                        await ctx.send(f"{ctx.author.name.lower()} [{clan.tag}]:")
                        await ctx.send(f"Current season points: {current_season_points}")
                        await ctx.send(f"{clan.tag} rank: {current_season_clan_rank}")
                        await ctx.send(f"Overall rank: {current_season_overall_rank}")
                        await ctx.send(f"Lifetime points: {lifetime_points}")
                else:
                    await ctx.send("You are not registered.")
            else:
                await ctx.send("No active seasons!")
        else:
            pass

    @commands.command()
    async def dates(self, ctx: commands.Context) -> None:
        """
        ?dates command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                season = await Season.active_seasons.all().filter(channel=channel).first()
                start_date = season.start_date.strftime("%d/%m/%Y")
                if season.info_end_date == None:
                    await ctx.send(
                        f"The current season started on {start_date} but doesn't have an end date yet."
                    )
                else:
                    end_date = season.info_end_date.strftime("%d/%m/%Y")
                    await ctx.send(
                        f"The current season started on {start_date} and ends on {end_date}."
                    )
            else:
                await ctx.send("There is no active season.")
        else:
            pass

    @commands.command()
    async def mvp(self, ctx: commands.Context) -> None:
        """
        ?mvp command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.all().filter(channel=channel).exists():
                previous_season = await Season.previous_seasons.filter(channel=channel).order_by("-end_date").first()
                await ctx.send(f"{previous_season.name}")
                if await Points.filter(channel=channel).filter(season=previous_season).exists():
                    points = await Points.filter(channel=channel).filter(season=previous_season).order_by("-points").first()
                    assert points is not None
                    player = await points.player.get()
                    assert player.clan is not None
                    await ctx.send(
                        f"Last season's Battle of Midgard MVP was {player.name} of {(await player.clan.get()).tag} with {points.points} points."
                    )
                else:
                    await ctx.send(f"No MVP for {previous_season.name}.")
            else:
                await ctx.send("There are no seasons.")
        else:
            pass

    @commands.command()
    async def checkin(self, ctx: commands.Context) -> None:
        """
        ?checkin command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                season = await Season.active_seasons.filter(channel=channel).first()
                if await Session.active_session.all().filter(channel=channel).exists():
                    session = await Session.active_session.filter(channel=channel).first()
                    if await Player.get_or_none(name=ctx.author.name.lower(), channel=channel):
                        player = await Player.get(name=ctx.author.name.lower(), channel=channel)
                        if player.is_enabled() and player.clan:
                            if await Checkin.get_or_none(player=player, session=session, channel=channel):
                                await ctx.send(f"@{ctx.author.name.lower()} has already checked in!")
                            else:
                                await Checkin.create(player=player, session=session, channel=channel)
                                clan = await player.clan.get()

                                ## We need to check if the checkin is within the first 30 minutes of the session, if so double the points given, if not, give normal points.
                                ## This is to encourage people to check in early and not just before the session ends.

                                ## Compare timezone aware datetime objects

                                if session.start_time + timedelta(minutes=30) > datetime.now(timezone.utc):
                                    points_to_give = 200
                                else:
                                    points_to_give = 100
                                
                                if await Points.get_or_none(player=player, season=season, channel=channel):
                                    points = await Points.get(player=player, season=season, channel=channel)
                                    points.points += points_to_give
                                    await points.save()
                                else:
                                    assert player.clan is not None
                                    await Points.create(
                                        player_id=player.id,
                                        season_id=season.id,
                                        points=points_to_give,
                                        clan_id=clan.id,
                                        channel=channel,
                                    )
                                
                                user_lifetime_checkins = await Checkin.filter(player=player, channel=channel).count()
                                if player.nickname:
                                    await ctx.send(f"@{ctx.author.name.lower()} ({player.nickname}) has checked in and earned {points_to_give} VP for the {clan.name.upper()}! HEIMDALL see's you watching! Total lifetime check-ins: ({user_lifetime_checkins})")
                                else:
                                    await ctx.send(f"@{ctx.author.name.lower()} has checked in and earned {points_to_give} VP for the {clan.name.upper()}! HEIMDALL see's you watching! Total lifetime check-ins: ({user_lifetime_checkins})")

                                discord_server = self.discord_bot.get_guild(self.twitch_bot.conf_options["APP"]["DISCORD_SERVER_ID"])
                                discord_channel = discord_server.get_channel(self.twitch_bot.conf_options["APP"]["DISCORD_CHECKINS_LOG_CHANNEL"])

                                await discord_channel.send(f"{ctx.author.name.lower()} has checked in for the {clan.name.upper()}! HEIMDALL see's them watching! Total lifetime check-ins: ({user_lifetime_checkins})")
                        else:
                            await ctx.send(f"@{ctx.author.name.lower()} is not in a Clan roster!")
                    else:
                        await ctx.send(f"@{ctx.author.name.lower()} is not in a clan roster!")
                else:
                    await ctx.send("No active session!")
            else:
                await ctx.send("No active seasons!")
        else:
            pass

    
    @commands.command()
    async def raid(self, ctx: commands.Context) -> None:
        """
        ?raid command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                season = await Season.active_seasons.filter(channel=channel).first()
                if await RaidSession.active_session.all().filter(channel=channel).exists():
                    session = await RaidSession.active_session.filter(channel=channel).first()
                    if await Player.get_or_none(name=ctx.author.name.lower(), channel=channel):
                        player = await Player.get(name=ctx.author.name.lower(), channel=channel)
                        if player.is_enabled() and player.clan:
                            if await RaidCheckin.get_or_none(player=player, session=session, channel=channel):
                                await ctx.send(f"@{ctx.author.name.lower()} is already in the raid boat! vander60RAIDBOAT")
                            else:
                                await RaidCheckin.create(player=player, session=session, channel=channel)
                                clan = await player.clan.get()
                                if await Points.get_or_none(player=player, season=season, channel=channel):
                                    points = await Points.get(player=player, season=season, channel=channel)
                                    points.points += 100
                                    await points.save()
                                else:
                                    assert player.clan is not None
                                    await Points.create(
                                        player_id=player.id,
                                        season_id=season.id,
                                        points=250,
                                        clan_id=clan.id,
                                        channel=channel,
                                    )
                                await ctx.send(f"vander60RAIDBOAT Hej @{ctx.author.name.lower()}, welcome aboard! vander60RAIDBOAT We set sail soon so sharpen your weapons and get ready to row! vander60RAIDBOAT")
                        else:
                            await ctx.send(f"@{ctx.author.name.lower()} is not in a Clan roster!")
                    else:
                        await ctx.send(f"@{ctx.author.name.lower()} is not in a clan roster!")
                else:
                    await ctx.send("No active session!")
            else:
                await ctx.send("No active seasons!")
        else:
            pass
    

    @commands.command()
    async def search(self, ctx: commands.Context, playername: str) -> None:
        """
        ?search command
        """

        ## This command should enter the follower giveaway for the user. Only one entry per user is allowed. If no playername is provided we will send an error message.

        if playername == "":
            await ctx.send(f"Type ?search @username in the chat to search new followers!")
        else:
            playername = playername.strip("@").lower()

        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await FollowerGiveaway.get_or_none(channel=channel, follower=playername):
                follower_giveaway = await FollowerGiveaway.get(channel=channel, follower=playername)
                # We need to check if the giveaway is still active by checking the end time.
                if follower_giveaway.end_time > datetime.now(timezone.utc):
                    if await Player.get_or_none(name=ctx.author.name.lower(), channel=channel):
                        player = await Player.get(name=ctx.author.name.lower(), channel=channel)
                        if await FollowerGiveawayEntry.get_or_none(giveaway=follower_giveaway, player=player, channel=channel):
                            pass
                        else:
                            await FollowerGiveawayEntry.create(giveaway=follower_giveaway, player=player, channel=channel)
                            await ctx.send(f"@{ctx.author.name.lower()} is searching...")
                    else:
                        pass
                else:
                    await ctx.send(f"The search is over!!")
            else:
                pass
        else:
            pass
    

    @commands.command()
    async def claim(self, ctx: commands.Context) -> None:
        """
        ?claim command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                season = await Season.active_seasons.filter(channel=channel).first()
                if await SpoilsSession.active_session.all().filter(channel=channel).exists():
                    session = await SpoilsSession.active_session.filter(channel=channel).first()
                    if await Player.get_or_none(name=ctx.author.name.lower(), channel=channel):
                        player = await Player.get(name=ctx.author.name.lower(), channel=channel)
                        if player.is_enabled() and player.clan:
                            if await SpoilsClaim.get_or_none(player=player, channel=channel, spoils_session=session):
                                await ctx.send(f"@{ctx.author.name.lower()} has already claimed the spoils!")
                            else:
                                await SpoilsClaim.create(player=player, channel=channel, spoils_session=session)
                                if await Points.get_or_none(player=player, season=season, channel=channel):
                                    points = await Points.get(player=player, season=season, channel=channel)
                                    points.points += session.points_reward
                                    await points.save()
                                else:
                                    await Points.create(
                                        player_id=player.id,
                                        season_id=season.id,
                                        points=session.points_reward,
                                        clan_id=0,
                                        channel=channel,
                                    )
                                await ctx.send(f"Thank you, @{ctx.author.name.lower()} for your aid on the battlefield! ⚔️ You have earned ({session.points_reward}) Valor Points!")
                        else:
                            pass
                    else:
                        pass
                else:
                    await ctx.send(f"Sorry @{ctx.author.name.lower()}, the next battle has begun!")
            else:
                pass
        else:
            pass


def prepare(twitch_bot: commands.Bot, discord_bot: discord_commands.Bot) -> None:
    twitch_bot.add_cog(BomCommandsCog(twitch_bot, discord_bot))
