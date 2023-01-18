from twitchio.ext import commands

from app.models import Channel


class BomBroadcasterCommandsCog(commands.Cog):
    def __init__(self, bot: commands.Cog) -> None:
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> bool:
        return ctx.author.is_broadcaster
    
    @commands.command()
    async def registerchannel(self, ctx: commands.Context) -> None:
        """
        !registerchannel command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            await ctx.send("This channel has already been registered.")
        else:
            await Channel.create(name=ctx.channel.name)
            await ctx.send("This channel has been registered.")

def prepare(bot: commands.Bot) -> None:
    bot.add_cog(BomBroadcasterCommandsCog(bot))