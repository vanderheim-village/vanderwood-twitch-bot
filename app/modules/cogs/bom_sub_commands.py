import random
from twitchio.ext import commands
from app.models import Clan, Player
from tortoise.functions import Count


class BomSubCommandsCog(commands.Cog):
    def __init__(self, bot: commands.Cog) -> None:
        self.bot = bot
    
    async def cog_check(self, ctx: commands.Context) -> bool:
        return ctx.author.is_subscriber or ctx.author.is_mod
    
    @commands.command()
    async def join(self, ctx: commands.Context) -> None:
        """
        !join command
        """

        if await Clan.all().count() == 0:
            await ctx.send("No clans have been created yet.")
        else:
            if await Player.filter(name=ctx.author.name).exists():
                await ctx.send("You have already joined a clan.")
            else:
                clan_totals = await Clan.all().annotate(count=Count("players", distinct=True)).values("id", "name", "tag", "count")
                min_total = min(clan_totals, key=lambda x:x["count"])
                clans_to_choose_from = [clan["id"] for clan in clan_totals if clan["count"] == min_total["count"]]
                new_clan = random.choice(clans_to_choose_from)
                await Player.create(name=ctx.author.name, clan_id=new_clan)
                clan_details = next(clan for clan in clan_totals if clan["id"] == new_clan)
                print(clan_details)
                await ctx.send(f"Welcome @{ctx.author.name} to the [{clan_details['tag']}] {clan_details['name']} Clan roster!")

def prepare(bot: commands.Bot) -> None:
    bot.add_cog(BomSubCommandsCog(bot))