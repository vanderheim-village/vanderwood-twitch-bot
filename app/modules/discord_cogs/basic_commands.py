import discord
from discord.ext import commands
from discord import app_commands

class BasicCommandsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="help", description="Get a list of commands which this bot supports.")
    async def help(self, interaction: discord.Interaction) -> None:
        """
        /help command
        """
        await interaction.response.send_message(
            f"You can view the list of commands which this bot supports here: {self.bot.conf_options['APP']['BOT_COMMANDS_LINK']}."
        )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BasicCommandsCog(bot))