from twitchio.ext import commands

from app.models import Checkin, Player, Points, Season, Session


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
        await ctx.send("Standings for current season.")

    @commands.command()
    async def overallrank(self, ctx: commands.Context) -> None:
        """
        !overallrank command
        """
        await ctx.send("Overall ranking for all players in current season.")

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
        await ctx.send("Dates for current season.")

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
