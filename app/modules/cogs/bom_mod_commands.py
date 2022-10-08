from twitchio.ext import commands

from app.models import Clan, Player, Season


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
        if await Clan.get_or_none(tag=clantag):
            clan = await Clan.get(tag=clantag)
            if await Player.get_or_none(name=playername):
                player = await Player.get(name=playername)
                if player.is_enabled():
                    player.select_for_update().update(clan_id=clan)
                    await ctx.send(
                        f"Welcome @{playername} to the [{clan.tag}] {clan.name} Clan roster!"
                    )
                else:
                    player.select_for_update().update(clan_id=clan, enabled=True)
                    await ctx.send(
                        f"Welcome @{playername} to the [{clan.tag}] {clan.name} Clan roster!"
                    )
            else:
                await Player.create(name=playername, clan=clan, enabled=True)
                await ctx.send(
                    f"Welcome @{playername} to the [{clan.tag}] {clan.name} Clan roster!"
                )
        else:
            await ctx.send(f"Clan {clantag} does not exist.")

    @commands.command()
    async def remove(self, ctx: commands.Context, playername: str) -> None:
        """
        !remove command
        """
        if await Player.get_or_none(name=playername):
            player = await Player.get(name=playername)
            if player.is_enabled():
                player.clan = None
                player.enabled = False
                await player.save()
                await ctx.send(f"Removed @{playername} from their clan!")
            else:
                await ctx.send(f"@{playername} is not in a Clan roster!")
        else:
            await ctx.send(f"@{playername} does not currently exist!")

    @commands.command()
    async def addpoints(self, ctx: commands.Context, playername: str, points: int) -> None:
        """
        !addpoints command
        """
        await ctx.send(f"Adding {points} points to {playername}.")

    @commands.command()
    async def removepoints(self, ctx: commands.Context, playername: str, points: int) -> None:
        """
        !removepoints command
        """
        await ctx.send(f"Removing {points} points from {playername}.")

    @commands.command()
    async def startseason(self, ctx: commands.Context, *, season_name: str) -> None:
        """
        !startseason command
        """
        if await Season.active_seasons.all().exists():
            await ctx.send("Battle of Midgard | A Season is already in progress.")
        else:
            await Season.create(name=season_name)
            await ctx.send(f"Battle of Midgard | {season_name} has commenced! Good luck!")

    @commands.command()
    async def endseason(self, ctx: commands.Context) -> None:
        """
        !endseason command
        """
        await ctx.send("Ending current season.")

    @commands.command()
    async def setdate(self, ctx: commands.Context, enddate: str) -> None:
        """
        !setdate command
        """
        await ctx.send(f"Setting end date to {enddate}.")

    @commands.command()
    async def createclan(self, ctx: commands.Context, clantag: str, *, clanname: str) -> None:
        """
        !createclan command
        """
        if len(clantag) <= 4:
            if await Clan.get_or_none(tag=clantag):
                if await Clan.get_or_none(name=clanname):
                    await ctx.send(
                        f"A clan with the name {clanname} and tag {clantag} already exists."
                    )
                else:
                    await ctx.send(f"A clan with the tag {clantag} already exists.")
            else:
                if await Clan.get_or_none(name=clanname):
                    await ctx.send(f"A clan with the name {clanname} already exists.")
                else:
                    await Clan.create(name=clanname, tag=clantag)
                    await ctx.send(f"Clan {clanname} with tag {clantag} has been created.")
        else:
            await ctx.send(f"Clan tag {clantag} is too long. It should be max 4 characters.")


def prepare(bot: commands.Bot) -> None:
    bot.add_cog(BomModCommandsCog(bot))
