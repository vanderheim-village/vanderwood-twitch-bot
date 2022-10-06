from twitchio.ext import commands
from app.models import Clan, Player
from tortoise.functions import Count

class BomModCommandsCog(commands.Cog):
    def __init__(self, bot: commands.Cog) -> None:
        self.bot = bot
    
    async def cog_check(self, ctx: commands.Context) -> bool:
        return ctx.author.is_mod
    
    @commands.command()
    async def add(self, ctx: commands.Context, clantag: str, playername: str) -> None:
        """
        !add command
        """
        if await Clan.get(tag=clantag).exists():
            clan_id = await Clan.get(tag=clantag)
            if (await Player.get(name=playername).exists()):
                await Player.get(name=playername).update(clan=clan_id)
                await ctx.send(f"@{playername} has been added to the {clantag} clan.")
            else:
                await Player.create(name=playername, clan=clan_id)
                await ctx.send(f"@{playername} has been added to the {clantag} clan.")
        else:
            await ctx.send(f"Clan {clantag} does not exist.")
            
    @commands.command()
    async def remove(self, ctx: commands.Context, clanname: str, playername: str) -> None:
        """
        !remove command
        """
        await ctx.send(
            f"Removing {playername} from {clanname}."
        )
    
    @commands.command()
    async def addpoints(self, ctx: commands.Context, playername: str, points: int) -> None:
        """
        !addpoints command
        """
        await ctx.send(
            f"Adding {points} points to {playername}."
        )
    
    @commands.command()
    async def removepoints(self, ctx: commands.Context, playername: str, points: int) -> None:
        """
        !removepoints command
        """
        await ctx.send(
            f"Removing {points} points from {playername}."
        )
    
    @commands.command()
    async def startseason(self, ctx: commands.Context) -> None:
        """
        !startseason command
        """
        await ctx.send(
            f"Starting new season."
        )
    
    @commands.command()
    async def endseason(self, ctx: commands.Context) -> None:
        """
        !endseason command
        """
        await ctx.send(
            f"Ending current season."
        )
    
    @commands.command()
    async def setdate(self, ctx: commands.Context, enddate: str) -> None:
        """
        !setdate command
        """
        await ctx.send(
            f"Setting end date to {enddate}."
        )

def prepare(bot: commands.Bot) -> None:
    bot.add_cog(BomModCommandsCog(bot))