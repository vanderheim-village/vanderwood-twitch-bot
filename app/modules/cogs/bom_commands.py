from typing import List, TypedDict

from tortoise.functions import Sum
from twitchio.ext import commands

from app.models import Checkin, Clan, Player, Points, Season, Session, Channel


class Standings(TypedDict):
    name: str
    points: int
    tag: str


class PlayerStandings(TypedDict):
    name: str
    points: int
    clantag: str


class BomCommandsCog(commands.Cog):
    def __init__(self, bot: commands.Cog) -> None:
        self.bot = bot

    @commands.command()
    async def rank(self, ctx: commands.Context, clanname: str) -> None:
        """
        !rank command

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
        !standings command
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
        !overallrank command
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
        !myrank command

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
                        if Points.get_or_none(player=player, season=active_season, channel=channel):
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

                        if Points.get_or_none(player=player, season=active_season, channel=channel):
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

                        if Points.get_or_none(player=player, season=active_season, channel=channel):
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
        !dates command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                season = await Season.active_seasons.all().filter(channel=channel).first()
                start_date = season.start_date.strftime("%d/%m/%Y")
                if season.end_date == None:
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
        !mvp command
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
        !checkin command
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
                                if await Points.get_or_none(player=player, season=season, channel=channel):
                                    points = await Points.get(player=player, season=season, channel=channel)
                                    points.points += 100
                                    await points.save()
                                else:
                                    assert player.clan is not None
                                    await Points.create(
                                        player_id=player.id,
                                        season_id=season.id,
                                        points=100,
                                        clan_id=clan.id,
                                        channel=channel,
                                    )
                                await ctx.send(f"@{ctx.author.name.lower()} has checked in!")
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


def prepare(bot: commands.Bot) -> None:
    bot.add_cog(BomCommandsCog(bot))
