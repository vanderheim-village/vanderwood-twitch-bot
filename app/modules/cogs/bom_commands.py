import logging
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, List, TypedDict

from discord.ext import commands as discord_commands
from tortoise.functions import Sum
from twitchio.ext import commands

from app.models import (
    Channel,
    Checkin,
    Clan,
    ClanSpoilsClaim,
    ClanSpoilsSession,
    FollowerGiveaway,
    FollowerGiveawayEntry,
    FollowerGiveawayPrize,
    GiftedSubsLeaderboard,
    Player,
    PlayerWatchTime,
    Points,
    RaidCheckin,
    RaidSession,
    Season,
    SentryCheckin,
    SentrySession,
    Session,
    SpoilsClaim,
    SpoilsSession,
)

if TYPE_CHECKING:
    from bot import DiscordBot, TwitchBot


logger = logging.getLogger(__name__)


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
                    for points_row in await Points.filter(
                        season=season, clan=clan, channel=channel
                    ):
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
                    await ctx.send(
                        f"{count}. [{result['tag']}] {result['name']} - {result['points']}"
                    )
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
                    active_season = (
                        await Season.active_seasons.all().filter(channel=channel).first()
                    )
                    assert player.clan is not None
                    if await player.clan.get() is None:
                        await ctx.send("You are not in a clan.")
                    else:
                        clan = await player.clan.get()
                        if await Points.get_or_none(
                            player=player, season=active_season, channel=channel
                        ):
                            current_season_points = (
                                await Points.get(
                                    player=player, season=active_season, channel=channel
                                )
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

                        if await Points.get_or_none(
                            player=player, season=active_season, channel=channel
                        ):
                            standings: List[PlayerStandings] = []
                            for points_row in await Points.filter(
                                season=active_season, channel=channel
                            ):
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

                        if await Points.get_or_none(
                            player=player, season=active_season, channel=channel
                        ):
                            clan_standings: List[PlayerStandings] = []
                            for points_row in await Points.filter(
                                season=active_season, clan=clan, channel=channel
                            ):
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
                previous_season = (
                    await Season.previous_seasons.filter(channel=channel)
                    .order_by("-end_date")
                    .first()
                )
                await ctx.send(f"{previous_season.name}")
                if await Points.filter(channel=channel).filter(season=previous_season).exists():
                    points = (
                        await Points.filter(channel=channel)
                        .filter(season=previous_season)
                        .order_by("-points")
                        .first()
                    )
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
                            if await Checkin.get_or_none(
                                player=player, session=session, channel=channel
                            ):
                                await ctx.send(
                                    f"@{ctx.author.name.lower()} has already checked in!"
                                )
                            else:
                                ## We need to check if the checkin is within the first 30 minutes of the session, if so double the points given, if not, give normal points.
                                ## This is to encourage people to check in early and not just before the session ends.
                                ## If the person is the first person to check in, give them 300 points instead of 200. Twitch moderators should be excluded from this and not count towards the first check-in.
                                ## They should get either 200 or 100 points depending on the time of check-in.

                                ## Compare timezone aware datetime objects

                                # broadcaster = await ctx.channel.user()
                                # mods = await broadcaster.fetch_moderators(self.twitch_bot.conf_options["APP"]["ACCESS_TOKEN"])

                                # list_of_mod_names = []

                                # for mod in mods:
                                #     list_of_mod_names.append(mod.name)

                                # list_of_checkins_except_mods = await Checkin.filter(session=session, channel=channel).exclude(player__name__in=list_of_mod_names)

                                # if len(list_of_checkins_except_mods) == 0:
                                #     points_to_give = 300
                                #
                                if (
                                    await Checkin.filter(session=session, channel=channel).count()
                                    == 0
                                ):
                                    points_to_give = 300
                                elif session.start_time + timedelta(minutes=30) > datetime.now(
                                    timezone.utc
                                ):
                                    points_to_give = 200
                                else:
                                    points_to_give = 100

                                await Checkin.create(
                                    player=player, session=session, channel=channel
                                )
                                clan = await player.clan.get()

                                if await Points.get_or_none(
                                    player=player, season=season, channel=channel
                                ):
                                    points = await Points.get(
                                        player=player, season=season, channel=channel
                                    )
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

                                user_lifetime_checkins = await Checkin.filter(
                                    player=player, channel=channel
                                ).count()
                                if player.nickname:
                                    await ctx.send(
                                        f"@{ctx.author.name.lower()} ({player.nickname}) has checked in and earned {points_to_give} VP for the {clan.name.upper()}! HEIMDALL see's you watching! Total lifetime check-ins: ({user_lifetime_checkins})"
                                    )
                                else:
                                    await ctx.send(
                                        f"@{ctx.author.name.lower()} has checked in and earned {points_to_give} VP for the {clan.name.upper()}! HEIMDALL see's you watching! Total lifetime check-ins: ({user_lifetime_checkins})"
                                    )

                                discord_server = self.discord_bot.get_guild(
                                    self.twitch_bot.conf_options["APP"]["DISCORD_SERVER_ID"]
                                )
                                discord_channel = discord_server.get_channel(
                                    self.twitch_bot.conf_options["APP"][
                                        "DISCORD_CHECKINS_LOG_CHANNEL"
                                    ]
                                )

                                await discord_channel.send(
                                    f"{ctx.author.name.lower()} has checked in for the {clan.name.upper()}! HEIMDALL see's them watching! Total lifetime check-ins: ({user_lifetime_checkins})"
                                )
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
                            if await RaidCheckin.get_or_none(
                                player=player, session=session, channel=channel
                            ):
                                await ctx.send(
                                    f"@{ctx.author.name.lower()} is already in the raid boat! vander60RAIDBOAT"
                                )
                            else:
                                await RaidCheckin.create(
                                    player=player, session=session, channel=channel
                                )
                                clan = await player.clan.get()
                                if await Points.get_or_none(
                                    player=player, season=season, channel=channel
                                ):
                                    points = await Points.get(
                                        player=player, season=season, channel=channel
                                    )
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
                                await ctx.send(
                                    f"vander60RAIDBOAT Hej @{ctx.author.name.lower()}, welcome aboard! vander60RAIDBOAT We set sail soon so sharpen your weapons and get ready to row! vander60RAIDBOAT"
                                )
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
                        if await FollowerGiveawayEntry.get_or_none(
                            giveaway=follower_giveaway, player=player, channel=channel
                        ):
                            pass
                        else:
                            await FollowerGiveawayEntry.create(
                                giveaway=follower_giveaway, player=player, channel=channel
                            )
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
                            if await SpoilsClaim.get_or_none(
                                player=player, channel=channel, spoils_session=session
                            ):
                                await ctx.send(
                                    f"@{ctx.author.name.lower()} has already claimed the spoils!"
                                )
                            else:
                                await SpoilsClaim.create(
                                    player=player, channel=channel, spoils_session=session
                                )
                                if await Points.get_or_none(
                                    player=player, season=season, channel=channel
                                ):
                                    points = await Points.get(
                                        player=player, season=season, channel=channel
                                    )
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
                                await ctx.send(
                                    f"Thank you, @{ctx.author.name.lower()} for your aid on the battlefield! ⚔️ You have claimed ({session.points_reward}) Valor Points!"
                                )
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

    @commands.command()
    async def clanclaim(self, ctx: commands.Context) -> None:
        """
        ?clanclaim command
        """

        ## We need to check the following:
        ## 1. If the channel exists.
        ## 2. If there is an active season.
        ## 3. If there is an active spoils session for the user's clan.
        ## 4. If the user is registered.
        ## 5. If the user has not claimed the spoils yet.

        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                season = await Season.active_seasons.filter(channel=channel).first()
                if await Player.get_or_none(name=ctx.author.name.lower(), channel=channel):
                    player = await Player.get(name=ctx.author.name.lower(), channel=channel)
                    if player.is_enabled() and player.clan:
                        clan = await player.clan.get()
                        if (
                            await ClanSpoilsSession.active_sessions.all()
                            .filter(channel=channel, clan=clan)
                            .exists()
                        ):
                            session = await ClanSpoilsSession.active_sessions.filter(
                                channel=channel, clan=clan
                            ).first()
                            if await ClanSpoilsClaim.get_or_none(
                                player=player, channel=channel, spoils_session=session
                            ):
                                await ctx.send(
                                    f"@{ctx.author.name.lower()} has already claimed the spoils!"
                                )
                            else:
                                await ClanSpoilsClaim.create(
                                    player=player, channel=channel, spoils_session=session
                                )
                                if await Points.get_or_none(
                                    player=player, season=season, channel=channel
                                ):
                                    points = await Points.get(
                                        player=player, season=season, channel=channel
                                    )
                                    points.points += session.points_reward
                                    await points.save()
                                else:
                                    await Points.create(
                                        player_id=player.id,
                                        season_id=season.id,
                                        points=session.points_reward,
                                        clan_id=clan.id,
                                        channel=channel,
                                    )
                                await ctx.send(
                                    f"Thank you, @{ctx.author.name.lower()} for your aid on the battlefield! ⚔️ You have claimed ({session.points_reward}) Valor Points for {clan.name.upper()}!"
                                )
                        else:
                            await ctx.send(
                                f"Sorry @{ctx.author.name.lower()}, the next battle has begun!"
                            )
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            pass

    @commands.command()
    async def sentry(self, ctx: commands.Context) -> None:
        """
        ?sentry command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                season = await Season.active_seasons.filter(channel=channel).first()
                if await SentrySession.active_session.all().filter(channel=channel).exists():
                    session = await SentrySession.active_session.filter(channel=channel).first()
                    if await Player.get_or_none(name=ctx.author.name.lower(), channel=channel):
                        player = await Player.get(name=ctx.author.name.lower(), channel=channel)
                        if player.is_enabled() and player.clan:
                            if await SentryCheckin.get_or_none(
                                player=player, session=session, channel=channel
                            ):
                                # The user has already checked in for the sentry session
                                pass
                            else:
                                await SentryCheckin.create(
                                    player=player, session=session, channel=channel
                                )
                                clan = await player.clan.get()
                                if await Points.get_or_none(
                                    player=player, season=season, channel=channel
                                ):
                                    points = await Points.get(
                                        player=player, season=season, channel=channel
                                    )
                                    points.points += 25
                                    await points.save()
                                else:
                                    assert player.clan is not None
                                    await Points.create(
                                        player_id=player.id,
                                        season_id=season.id,
                                        points=25,
                                        clan_id=clan.id,
                                        channel=channel,
                                    )

                                if await PlayerWatchTime.get_or_none(
                                    player=player, channel=channel, season=season
                                ):
                                    watchtime = await PlayerWatchTime.get(
                                        player=player, channel=channel, season=season
                                    )
                                    watchtime.watch_time += 30
                                    await watchtime.save()
                                else:
                                    await PlayerWatchTime.create(
                                        player_id=player.id,
                                        channel_id=channel.id,
                                        season_id=season.id,
                                        watch_time=30,
                                    )

                                await ctx.send(
                                    f"🏹 👁️ @{ctx.author.name.lower()} is watching... (+25 VP ⌛ {watchtime.watch_time / 60}hrs)"
                                )
                        else:
                            await ctx.send(f"@{ctx.author.name.lower()} is not in a Clan roster!")
                    else:
                        await ctx.send(f"@{ctx.author.name.lower()} is not in a clan roster!")
                else:
                    next_run_time = self.twitch_bot.start_sentry_session.next_run
                    minutes_until_next_run = (
                        next_run_time - datetime.now(timezone.utc)
                    ).seconds // 60
                    await ctx.send(
                        f"Sorry @{ctx.author.name.lower()}, the watch has already begun! The next ?sentry call is in {minutes_until_next_run} minutes!"
                    )
            else:
                await ctx.send("No active seasons!")
        else:
            pass

    @commands.command()
    async def profile(self, ctx: commands.Context) -> None:
        """
        ?profile command

        Display current season points, lifetime points, current season rank in clan and overall rank for current season, checkins, raids, sentry time in hours and gift subs.
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                if await Player.get_or_none(name=ctx.author.name.lower(), channel=channel):
                    player = await Player.get(name=ctx.author.name.lower(), channel=channel)
                    actual_player_object = await Player.get(
                        name=ctx.author.name.lower(), channel=channel
                    )
                    active_season = (
                        await Season.active_seasons.all().filter(channel=channel).first()
                    )
                    assert player.clan is not None
                    if await player.clan.get() is None:
                        await ctx.send("You are not in a clan.")
                    else:
                        clan = await player.clan.get()
                        if await Points.get_or_none(
                            player=player, season=active_season, channel=channel
                        ):
                            current_season_points = (
                                await Points.get(
                                    player=player, season=active_season, channel=channel
                                )
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

                        if await Points.get_or_none(
                            player=player, season=active_season, channel=channel
                        ):
                            standings: List[PlayerStandings] = []
                            for points_row in await Points.filter(
                                season=active_season, channel=channel
                            ):
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

                        if await Points.get_or_none(
                            player=player, season=active_season, channel=channel
                        ):
                            clan_standings: List[PlayerStandings] = []
                            for points_row in await Points.filter(
                                season=active_season, clan=clan, channel=channel
                            ):
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

                        checkins = await Checkin.filter(
                            player=actual_player_object, channel=channel
                        ).count()
                        raids = await RaidCheckin.filter(
                            player=actual_player_object, channel=channel
                        ).count()
                        sentry_watchtimes = await PlayerWatchTime.filter(
                            player=actual_player_object, channel=channel, season=active_season
                        ).values_list("watch_time")
                        total_sentry_watchtime = 0
                        for watchtime in sentry_watchtimes:
                            total_sentry_watchtime += watchtime[0]
                        # total sentry watchtime in hours and should support .5 hours as sentry is calculated in 30 minute intervals.
                        logger.info(f"Total sentry watchtime: {total_sentry_watchtime}")
                        total_sentry_watchtime_hours = total_sentry_watchtime / 60
                        logger.info(
                            f"Total sentry watchtime in hours: {total_sentry_watchtime_hours}"
                        )

                        if await GiftedSubsLeaderboard.get_or_none(
                            player=actual_player_object, channel=channel
                        ):
                            gifted_subs = (
                                await GiftedSubsLeaderboard.get(
                                    player=actual_player_object, channel=channel
                                )
                            ).gifted_subs
                        else:
                            gifted_subs = 0

                        await ctx.send(
                            f"{clan.twitch_emoji_name} [{clan.tag}] {actual_player_object.name.upper()} (RANKS - CLAN: {current_season_clan_rank} | OVERALL: {current_season_overall_rank}) | SEASON VP: {current_season_points} | LIFETIME VP: {lifetime_points} | CHECKINS: {checkins} | RAIDS: {raids} | ?SENTRY TIME: {total_sentry_watchtime_hours}hrs | GIFTED SUBS: {gifted_subs} {clan.twitch_emoji_name}"
                        )
                else:
                    await ctx.send("You are not registered.")
            else:
                await ctx.send("No active seasons!")
        else:
            pass


def prepare(twitch_bot: commands.Bot, discord_bot: discord_commands.Bot) -> None:
    twitch_bot.add_cog(BomCommandsCog(twitch_bot, discord_bot))
