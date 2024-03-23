from twitchio.ext import commands
from discord.ext import commands as discord_commands


class BasicCommandsCog(commands.Cog):
    def __init__(self, twitch_bot: commands.Cog, discord_bot: discord_commands.Bot) -> None:
        self.twitch_bot = twitch_bot
        self.discord_bot = discord_bot

    @commands.command(aliases=["commands"])
    async def help(self, ctx: commands.Context) -> None:
        """
        ?help (?commands) command
        """
        await self.discord_bot.log_message("The ?help command was used.")
        await ctx.send(
            f"You can view the list of commands which this bot supports here: {self.twitch_bot.conf_options['APP']['BOT_COMMANDS_LINK']}."
        )


def prepare(twitch_bot: commands.Bot, discord_bot: discord_commands.Bot) -> None:
    twitch_bot.add_cog(BasicCommandsCog(twitch_bot, discord_bot))
