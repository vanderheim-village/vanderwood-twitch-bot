from twitchio.ext import commands


class BasicCommandsCog(commands.Cog):
    def __init__(self, bot: commands.Cog) -> None:
        self.bot = bot

    @commands.command(aliases=["commands"])
    async def help(self, ctx: commands.Context) -> None:
        """
        !help (!commands) command
        """
        await ctx.send(
            f"You can view the list of commands which this bot supports here: {self.bot.conf_options['APP']['BOT_COMMANDS_LINK']}."
        )


def prepare(bot: commands.Bot) -> None:
    bot.add_cog(BasicCommandsCog(bot))
