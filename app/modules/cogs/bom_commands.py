from twitchio.ext import commands


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
        await ctx.send(f"Checking in {ctx.author.name}.")

    @commands.command()
    async def myrewards(self, ctx: commands.Context) -> None:
        """
        !myrewards command
        """
        await ctx.send(f"Rewards for {ctx.author.name}.")


def prepare(bot: commands.Bot) -> None:
    bot.add_cog(BomCommandsCog(bot))
