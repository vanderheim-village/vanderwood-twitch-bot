from datetime import datetime, timezone

import pytz
from discord.ext import commands as discord_commands
from twitchio.ext import commands


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

    @commands.command()
    async def vandertime(self, ctx: commands.Context) -> None:
        """
        ?vandertime command

        Display the localtime for the Vanderheim which is the Melbourne, Australia timezone.

        Lets display in the format: Monday 1st May 2024 1:30 PM
        """

        await ctx.send(
            f"The current time in Vanderheim is: {datetime.now(timezone.utc).astimezone(pytz.timezone('Australia/Melbourne')).strftime('%A %d %B %Y %I:%M %p')}"
        )


def prepare(twitch_bot: commands.Bot, discord_bot: discord_commands.Bot) -> None:
    twitch_bot.add_cog(BasicCommandsCog(twitch_bot, discord_bot))
