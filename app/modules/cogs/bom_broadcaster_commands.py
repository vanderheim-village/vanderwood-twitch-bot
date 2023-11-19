from twitchio.ext import commands
from discord.ext import commands as discord_commands

from app.models import Channel


class BomBroadcasterCommandsCog(commands.Cog):
    def __init__(self, twitch_bot: commands.Cog, discord_bot: discord_commands.Bot) -> None:
        self.twitch_bot = twitch_bot
        self.discord_bot = discord_bot

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

def prepare(twitch_bot: commands.Bot, discord_bot: discord_commands.Bot) -> None:
    twitch_bot.add_cog(BomBroadcasterCommandsCog(twitch_bot, discord_bot))