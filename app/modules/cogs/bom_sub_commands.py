import random

from tortoise.functions import Count
from twitchio.ext import commands
from discord.ext import commands as discord_commands

from app.models import Clan, Player, Channel


class BomSubCommandsCog(commands.Cog):
    def __init__(self, twitch_bot: commands.Cog, discord_bot: discord_commands.Bot) -> None:
        self.twitch_bot = twitch_bot
        self.discord_bot = discord_bot

    async def cog_check(self, ctx: commands.Context) -> bool:
        return ctx.author.is_subscriber or ctx.author.is_mod

    @commands.command()
    async def join(self, ctx: commands.Context) -> None:
        """
        ?join command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Clan.all().filter(channel=channel).count() == 0:
                await ctx.send("No clans have been created yet.")
            else:
                if await Player.filter(name=ctx.author.name.lower(), channel=channel).exists():
                    player = await Player.get(name=ctx.author.name.lower(), channel=channel)
                    if player.is_enabled():
                        clan = await Clan.get(id=player.clan_id)
                        clan_details = await Clan.get(id=clan.id)
                        await ctx.send(
                            f"Welcome @{ctx.author.name.lower()} to the [{clan_details.tag}] {clan_details.name} Clan roster!"
                        )
                    else:
                        await ctx.send(
                            f"@{ctx.author.name.lower()} you are currently disabled, please contact a moderator to enable you."
                        )
                else:
                    clan_totals = (
                        await Clan.all()
                        .filter(channel=channel)
                        .annotate(count=Count("players", distinct=True))
                        .values("id", "name", "tag", "count")
                    )
                    min_total = min(clan_totals, key=lambda x: x["count"])
                    clans_to_choose_from = [
                        clan["id"] for clan in clan_totals if clan["count"] == min_total["count"]
                    ]
                    new_clan = random.choice(clans_to_choose_from)
                    await Player.create(name=ctx.author.name.lower(), clan_id=new_clan, channel=channel)
                    clan_details = next(clan for clan in clan_totals if clan["id"] == new_clan)
                    print(clan_details)
                    await ctx.send(
                        f"Welcome @{ctx.author.name.lower()} to the [{clan_details['tag']}] {clan_details['name']} Clan roster!"
                    )
        else:
            pass


def prepare(twitch_bot: commands.Bot, discord_bot: discord_commands.Bot) -> None:
    twitch_bot.add_cog(BomSubCommandsCog(twitch_bot, discord_bot))
