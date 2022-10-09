from typing import List, TypedDict

from twitchio.ext import commands

from app.models import Checkin, Clan, Player, Points, Season, Session


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
        """
        await ctx.send(f"Ranking for {clanname}.")

    @commands.command()
    async def standings(self, ctx: commands.Context) -> None:
        """
        !standings command
        """
        if await Season.active_seasons.all().exists():
            season = await Season.active_seasons.all().first()
            standings: List[Standings] = []
            for clan in await Clan.all():
                clan_standings: Standings = {
                    "points": 0,
                    "name": clan.name,
                    "tag": clan.tag,
                }
                for points in await Points.filter(season=season, clan=clan):
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

    @commands.command()
    async def overallrank(self, ctx: commands.Context) -> None:
        """
        !overallrank command
        """
        if await Season.active_seasons.all().exists():
            season = await Season.active_seasons.all().first()
            standings: List[PlayerStandings] = []
            for points_row in await Points.filter(season=season):
                player = await points_row.player.get()
                assert player.clan is not None
                player_standings: PlayerStandings = {
                    "points": points_row.points,
                    "name": player.name,
                    "clantag": player.clan.tag,
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

    @commands.command()
    async def myrank(self, ctx: commands.Context) -> None:
        """
        !myrank command
        """
        await ctx.send(f"Ranking for {ctx.author.name}.")

    @commands.command()
    async def clanchampions(self, ctx: commands.Context) -> None:
        """
        !clanchampions command
        """
        await ctx.send("Clan champions for each clan")

    @commands.command()
    async def dates(self, ctx: commands.Context) -> None:
        """
        !dates command
        """
        if await Season.active_seasons.all().exists():
            season = await Season.active_seasons.all().first()
            start_date = season.start_date.strftime("%d/%m/%Y")
            if season.end_date == None:
                await ctx.send(
                    f"The current season started on {start_date} but doesn't have an end date yet."
                )
            else:
                end_date = season.end_date.strftime("%d/%m/%Y")
                await ctx.send(
                    f"The current season started on {start_date} and ends on {end_date}."
                )
        else:
            await ctx.send("There is no active season.")

    @commands.command()
    async def mvp(self, ctx: commands.Context) -> None:
        """
        !mvp command
        """
        await ctx.send("MVP for last season.")

    @commands.command()
    async def checkin(self, ctx: commands.Context) -> None:
        """
        !checkin command
        """
        if await Season.active_seasons.all().exists():
            season = await Season.active_seasons.first()
            if await Session.active_session.all().exists():
                session = await Session.active_session.first()
                if await Player.get_or_none(name=ctx.author.name):
                    player = await Player.get(name=ctx.author.name)
                    if player.is_enabled() and player.clan:
                        if await Checkin.get_or_none(player=player, session=session):
                            await ctx.send(f"@{ctx.author.name} has already checked in!")
                        else:
                            await Checkin.create(player=player, session=session)
                            clan = await player.clan.get()
                            if await Points.get_or_none(player=player, season=season):
                                points = await Points.get(player=player, season=season)
                                points.points += 100
                                await points.save()
                            else:
                                assert player.clan is not None
                                await Points.create(
                                    player_id=player.id,
                                    season_id=season.id,
                                    points=100,
                                    clan_id=clan.id,
                                )
                            await ctx.send(f"@{ctx.author.name} has checked in!")
                    else:
                        await ctx.send(f"@{ctx.author.name} is not in a Clan roster!")
                else:
                    await ctx.send(f"@{ctx.author.name} is not in a clan roster!")
            else:
                await ctx.send("No active session!")
        else:
            await ctx.send("No active seasons!")

    @commands.command()
    async def myrewards(self, ctx: commands.Context) -> None:
        """
        !myrewards command
        """
        await ctx.send(f"Rewards for {ctx.author.name}.")


def prepare(bot: commands.Bot) -> None:
    bot.add_cog(BomCommandsCog(bot))
