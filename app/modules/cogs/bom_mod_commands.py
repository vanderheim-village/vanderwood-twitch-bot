from datetime import datetime

from tortoise import timezone
from twitchio.ext import commands

from app.helpers import date_validate
from app.models import Clan, Player, Points, Season, Session


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
            if await Player.get_or_none(name=playername.lower()):
                if await Season.active_seasons.all().exists():
                    await ctx.send("Cannot move players between clans during an active season.")
                else:
                    player = await Player.get(name=playername.lower())
                    if player.is_enabled():
                        player.clan = clan
                        await player.save()
                        await ctx.send(
                            f"Welcome @{playername.lower()} to the [{clan.tag}] {clan.name} Clan roster!"
                        )
                    else:
                        player.clan = clan
                        await player.save()
                        await ctx.send(
                            f"Welcome @{playername.lower()} to the [{clan.tag}] {clan.name} Clan roster!"
                        )
            else:
                await Player.create(name=playername.lower(), clan=clan, enabled=True)
                await ctx.send(
                    f"Welcome @{playername.lower()} to the [{clan.tag}] {clan.name} Clan roster!"
                )
        else:
            await ctx.send(f"Clan {clantag} does not exist.")

    @commands.command()
    async def remove(self, ctx: commands.Context, playername: str) -> None:
        """
        !remove command
        """
        if await Player.get_or_none(name=playername.lower()):
            player = await Player.get(name=playername.lower())
            if player.is_enabled():
                player.clan = None
                player.enabled = False
                await player.save()
                await ctx.send(f"Removed @{playername.lower()} from their clan!")
            else:
                await ctx.send(f"@{playername.lower()} is not in a Clan roster!")
        else:
            await ctx.send(f"@{playername.lower()} does not currently exist!")

    @commands.command()
    async def addpoints(self, ctx: commands.Context, playername: str, newpoints: int) -> None:
        """
        !addpoints command
        """
        if await Season.active_seasons.all().exists():
            season: Season = await Season.active_seasons.all().first()
            if await Player.get_or_none(name=playername.lower()):
                player = await Player.get(name=playername.lower())
                if player.is_enabled() and player.clan:
                    clan = await player.clan.get()
                    if await Points.get_or_none(player=player, season=season):
                        points = await Points.get(player=player, season=season)
                        points.points += newpoints
                        await points.save()
                        await ctx.send(
                            f"Added {newpoints} points to @{playername.lower()} for the {season.name} season!"
                        )
                    else:
                        assert player.clan is not None
                        await Points.create(
                            player_id=player.id,
                            season_id=season.id,
                            points=newpoints,
                            clan_id=clan.id,
                        )
                        await ctx.send(
                            f"Added {newpoints} points to @{playername.lower()} for the {season.name} season!"
                        )
                else:
                    await ctx.send(f"@{playername.lower()} is not in a Clan roster!")
            else:
                await ctx.send(f"@{playername.lower()} is not in a Clan roster!")
        else:
            await ctx.send("No active seasons!")

    @commands.command()
    async def removepoints(self, ctx: commands.Context, playername: str, losepoints: int) -> None:
        """
        !removepoints command
        """
        if await Season.active_seasons.all().exists():
            season: Season = await Season.active_seasons.all().first()
            if await Player.get_or_none(name=playername.lower()):
                player = await Player.get(name=playername.lower())
                if player.is_enabled() and player.clan:
                    if await Points.get_or_none(player=player, season=season):
                        points = await Points.get(player=player, season=season)
                        newpoints = points.points - losepoints
                        if newpoints <= 0:
                            points.points = 0
                        else:
                            points.points -= losepoints
                        await points.save()
                        await ctx.send(
                            f"Removed {losepoints} points from @{playername.lower()} for the {season.name} season!"
                        )
                    else:
                        await ctx.send(f"@{playername.lower()} has no points for the {season.name} season!")
                else:
                    await ctx.send(f"@{playername.lower()} is not in a Clan roster!")
            else:
                await ctx.send(f"@{playername.lower()} is not in a Clan roster!")
        else:
            await ctx.send("No active seasons!")

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
        if await Season.active_seasons.all().exists():
            if await Session.active_session.all().exists():
                await ctx.send("Please end the current session first!")
            else:
                active_season = await Season.active_seasons.all().first()
                await Season.active_seasons.all().update(end_date=timezone.now())
                await ctx.send(
                    f"Battle of Midgard | {active_season.name} has ended. The results will be posted shortly! Thank you to everyone for a great season!"
                )
        else:
            await ctx.send("Battle of Midgard | No Season is currently in progress.")

    @commands.command()
    async def setdate(self, ctx: commands.Context, enddate: str) -> None:
        """
        !setdate command
        """
        if await date_validate(enddate):
            if await Season.active_seasons.all().exists():
                active_season: Season = await Season.active_seasons.all().first()
                date = datetime.strptime(enddate, "%d/%m/%Y")
                date = timezone.make_aware(date)
                await active_season.select_for_update().update(info_end_date=date)
                await ctx.send(f"Battle of Midgard | {active_season.name} will end on {enddate}.")
            else:
                await ctx.send("Battle of Midgard | No Season is currently in progress.")
        else:
            await ctx.send("Invalid date format. Please use DD/MM/YYYY.")

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

    @commands.command()
    async def startsession(self, ctx: commands.Context) -> None:
        """
        !startsession command
        """
        if await Season.active_seasons.all().exists():
            active_season: Season = await Season.active_seasons.all().first()
            if await Session.active_session.all().exists():
                await ctx.send("A session is already in progress.")
            else:
                await Session.create(season=active_season)
                await ctx.send("A session has been created for the current season.")
        else:
            await ctx.send("No active seasons!")

    @commands.command()
    async def endsession(self, ctx: commands.Context) -> None:
        """
        !endsession command
        """
        if await Season.active_seasons.all().exists():
            if await Session.active_session.all().exists():
                await Session.active_session.all().update(end_time=timezone.now())
                await ctx.send("The current session has been ended.")
            else:
                await ctx.send("No session is currently in progress.")
        else:
            await ctx.send("No active seasons!")


def prepare(bot: commands.Bot) -> None:
    bot.add_cog(BomModCommandsCog(bot))
