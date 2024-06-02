from datetime import datetime

from tortoise import timezone
from twitchio.ext import commands
from discord.ext import commands as discord_commands
import time

from app.helpers import date_validate
from app.models import Clan, Player, Points, Season, Session, Channel, RewardLevel, RaidSession, RaidCheckin

import logging

logger = logging.getLogger(__name__)

class BomModCommandsCog(commands.Cog):
    def __init__(self, twitch_bot: commands.Cog, discord_bot: discord_commands.Bot) -> None:
        self.twitch_bot = twitch_bot
        self.discord_bot = discord_bot

    async def cog_check(self, ctx: commands.Context) -> bool:
        return ctx.author.is_mod

    @commands.command()
    async def boatcheck(self, ctx: commands.Context) -> None:
        """
        ?boatcheck command
        
        Check how many people have checked in for the current raid session.
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await RaidSession.active_session.all().filter(channel=channel).exists():
                raid_session = await RaidSession.active_session.all().filter(channel=channel).first()
                checkins = await RaidCheckin.all().filter(session=raid_session)
                await ctx.send(f"{len(checkins)} vikings have got in the boats for the raid! vander60RAIDBOAT Use ?raid to get in the boats and earn your Tag of Ægir! Get ready to row! 🚣🚣🚣")
            else:
                await ctx.send("No raid is currently in progress.")
        else:
            pass

    @commands.cooldown(rate=3, per=300, bucket=commands.Bucket.channel)
    @commands.command()
    async def clip(self, ctx: commands.Context) -> None:
        """
        ?clip command
        """
        response = await self.twitch_bot.session.get(self.twitch_bot.conf_options["APP"]["CLIP_API_URL"])

        time.sleep(3)

        text = await response.text()
        
        await ctx.send(text)

    @commands.command()
    async def add(self, ctx: commands.Context, clantag: str, playername: str) -> None:
        """
        ?add command
        """

        playername = playername.strip("@")

        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Clan.get_or_none(tag=clantag, channel=channel):
                clan = await Clan.get(tag=clantag, channel=channel)
                if await Player.get_or_none(name=playername.lower(), channel=channel):
                    if await Season.active_seasons.all().filter(channel=channel).exists():
                        await ctx.send("Cannot move players between clans during an active season.")
                    else:
                        player = await Player.get(name=playername.lower(), channel=channel)
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
                    await Player.create(name=playername.lower(), clan=clan, enabled=True, channel=channel)
                    await ctx.send(
                        f"Welcome @{playername.lower()} to the [{clan.tag}] {clan.name} Clan roster!"
                    )
            else:
                await ctx.send(f"Clan {clantag} does not exist.")
        else:
            pass

    @commands.command()
    async def remove(self, ctx: commands.Context, playername: str) -> None:
        """
        ?remove command
        """

        playername = playername.strip("@")

        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Player.get_or_none(name=playername.lower(), channel=channel):
                player = await Player.get(name=playername.lower(), channel=channel)
                if player.is_enabled():
                    player.clan = None
                    player.enabled = False
                    await player.save()
                    await ctx.send(f"Removed @{playername.lower()} from their clan!")
                else:
                    await ctx.send(f"@{playername.lower()} is not in a Clan roster!")
            else:
                await ctx.send(f"@{playername.lower()} does not currently exist!")
        else:
            pass

    @commands.command()
    async def addvp(self, ctx: commands.Context, playername: str, newpoints: int) -> None:
        """
        ?addvp command
        """

        playername = playername.strip("@")

        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                season: Season = await Season.active_seasons.all().filter(channel=channel).first()
                if await Player.get_or_none(name=playername.lower(), channel=channel):
                    player = await Player.get(name=playername.lower(), channel=channel)
                    if player.is_enabled() and player.clan:
                        clan = await player.clan.get()
                        if await Points.get_or_none(player=player, season=season, channel=channel):
                            points = await Points.get(player=player, season=season, channel=channel)
                            points.points += newpoints
                            await points.save()
                            await ctx.send(
                                f"Added {newpoints} valor points to @{playername.lower()} for the {season.name} season!"
                            )
                        else:
                            assert player.clan is not None
                            await Points.create(
                                player_id=player.id,
                                season_id=season.id,
                                points=newpoints,
                                clan_id=clan.id,
                                channel=channel,
                            )
                            await ctx.send(
                                f"Added {newpoints} valor points to @{playername.lower()} for the {season.name} season!"
                            )
                    else:
                        await ctx.send(f"@{playername.lower()} is not in a Clan roster!")
                else:
                    await ctx.send(f"@{playername.lower()} is not in a Clan roster!")
            else:
                await ctx.send("No active seasons!")
        else:
            pass

    @commands.command()
    async def removevp(self, ctx: commands.Context, playername: str, losepoints: int) -> None:
        """
        ?removevp command
        """

        playername = playername.strip("@")

        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                season: Season = await Season.active_seasons.all().filter(channel=channel).first()
                if await Player.get_or_none(name=playername.lower(), channel=channel):
                    player = await Player.get(name=playername.lower(), channel=channel)
                    if player.is_enabled() and player.clan:
                        if await Points.get_or_none(player=player, season=season, channel=channel):
                            points = await Points.get(player=player, season=season, channel=channel)
                            newpoints = points.points - losepoints
                            if newpoints <= 0:
                                points.points = 0
                            else:
                                points.points -= losepoints
                            await points.save()
                            await ctx.send(
                                f"Removed {losepoints} valor points from @{playername.lower()} for the {season.name} season!"
                            )
                        else:
                            await ctx.send(f"@{playername.lower()} has no valor points for the {season.name} season!")
                    else:
                        await ctx.send(f"@{playername.lower()} is not in a Clan roster!")
                else:
                    await ctx.send(f"@{playername.lower()} is not in a Clan roster!")
            else:
                await ctx.send("No active seasons!")
        else:
            pass

    @commands.command()
    async def startseason(self, ctx: commands.Context, *, season_name: str) -> None:
        """
        ?startseason command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                await ctx.send("Battle of Midgard | A Season is already in progress.")
            else:
                await Season.create(name=season_name, channel=channel)
                await ctx.send(f"Battle of Midgard | {season_name} has commenced! Good luck!")
        else:
            pass

    @commands.command()
    async def endseason(self, ctx: commands.Context) -> None:
        """
        ?endseason command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                if await Session.active_session.all().filter(channel=channel).exists():
                    await ctx.send("Please end the current session first!")
                else:
                    active_season = await Season.active_seasons.all().filter(channel=channel).first()
                    await Season.active_seasons.all().filter(channel=channel).update(end_date=timezone.now())
                    await ctx.send(
                        f"Battle of Midgard | {active_season.name} has ended. The results will be posted shortly! Thank you to everyone for a great season!"
                    )
            else:
                await ctx.send("Battle of Midgard | No Season is currently in progress.")
        else:
            pass

    @commands.command()
    async def setdate(self, ctx: commands.Context, enddate: str) -> None:
        """
        ?setdate command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await date_validate(enddate):
                if await Season.active_seasons.all().filter(channel=channel).exists():
                    active_season: Season = await Season.active_seasons.all().filter(channel=channel).first()
                    date = datetime.strptime(enddate, "%d/%m/%Y")
                    date = timezone.make_aware(date)
                    await active_season.select_for_update().update(info_end_date=date)
                    await ctx.send(f"Battle of Midgard | {active_season.name} will end on {enddate}.")
                else:
                    await ctx.send("Battle of Midgard | No Season is currently in progress.")
            else:
                await ctx.send("Invalid date format. Please use DD/MM/YYYY.")
        else:
            pass

    @commands.command()
    async def createclan(self, ctx: commands.Context, clantag: str, *, clanname: str) -> None:
        """
        ?createclan command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if len(clantag) <= 4:
                if await Clan.get_or_none(tag=clantag, channel=channel):
                    if await Clan.get_or_none(name=clanname, channel=channel):
                        await ctx.send(
                            f"A clan with the name {clanname} and tag {clantag} already exists."
                        )
                    else:
                        await ctx.send(f"A clan with the tag {clantag} already exists.")
                else:
                    if await Clan.get_or_none(name=clanname, channel=channel):
                        await ctx.send(f"A clan with the name {clanname} already exists.")
                    else:
                        await Clan.create(name=clanname, tag=clantag, channel=channel)
                        await ctx.send(f"Clan {clanname} with tag {clantag} has been created.")
            else:
                await ctx.send(f"Clan tag {clantag} is too long. It should be max 4 characters.")
        else:
            pass

    @commands.command()
    async def startsession(self, ctx: commands.Context) -> None:
        """
        ?startsession command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                active_season: Season = await Season.active_seasons.all().filter(channel=channel).first()
                if await Session.active_session.all().filter(channel=channel).exists():
                    await ctx.send("A session is already in progress.")
                else:
                    await Session.create(season=active_season, channel=channel)
                    await ctx.send("A session has been created for the current season.")
            else:
                await ctx.send("No active seasons!")
        else:
            pass

    @commands.command()
    async def startraid(self, ctx: commands.Context) -> None:
        """
        ?startraid command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                active_season: Season = await Season.active_seasons.all().filter(channel=channel).first()
                if await RaidSession.active_session.all().filter(channel=channel).exists():
                    await ctx.send("A raid is already in progress.")
                else:
                    await RaidSession.create(season=active_season, channel=channel)
                    await ctx.send("vander60RAIDBOAT The raiding party has begun! vander60RAIDBOAT Use ?raid to get in the boats and earn your Tag of Ægir! Get ready to row! 🚣🚣🚣")
            else:
                await ctx.send("No active seasons!")
        else:
            pass

    @commands.command()
    async def endsession(self, ctx: commands.Context) -> None:
        """
        ?endsession command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                if await Session.active_session.all().filter(channel=channel).exists():
                    await Session.active_session.all().filter(channel=channel).update(end_time=timezone.now())
                    await ctx.send("The current session has been ended.")
                else:
                    await ctx.send("No session is currently in progress.")
            else:
                await ctx.send("No active seasons!")
        else:
            pass
    

    @commands.command()
    async def endraid(self, ctx: commands.Context) -> None:
        """
        ?endraid command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await Season.active_seasons.all().filter(channel=channel).exists():
                if await RaidSession.active_session.all().filter(channel=channel).exists():
                    await RaidSession.active_session.all().filter(channel=channel).update(end_time=timezone.now())
                    await ctx.send("The raiding party is over!")
                else:
                    await ctx.send("No raid is currently in progress.")
            else:
                await ctx.send("No active seasons!")
        else:
            pass
    
    @commands.command()
    async def addrewardlevel(self, ctx: commands.Context, level: int, *, reward: str) -> None:
        """
        ?addrewardlevel command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await RewardLevel.get_or_none(level=level, channel=channel):
                await ctx.send(f"Reward level {level} already exists.")
            else:
                await RewardLevel.create(level=level, reward=reward, channel=channel)
                await ctx.send(f"Reward level {level} has been created.")
        else:
            pass
    
    @commands.command()
    async def editrewardlevel(self, ctx: commands.Context, level: int, *, reward: str) -> None:
        """
        ?editrewardlevel command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await RewardLevel.get_or_none(level=level, channel=channel):
                await (await RewardLevel.get(level=level, channel=channel)).update(reward=reward)
                await ctx.send(f"Reward level {level} has been updated.")
            else:
                await ctx.send(f"Reward level {level} does not exist.")
        else:
            pass
    
    @commands.command()
    async def removerewardlevel(self, ctx: commands.Context, level: int) -> None:
        """
        ?removerewardlevel command
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            if await RewardLevel.get_or_none(level=level, channel=channel):
                await (await RewardLevel.get(level=level, channel=channel)).delete()
                await ctx.send(f"Reward level {level} has been deleted.")
            else:
                await ctx.send(f"Reward level {level} does not exist.")
        else:
            pass
    
    @commands.command()
    async def lucky(self, ctx: commands.Context, playername: str) -> None:
        """
        ?lucky command
        
        This commands will post a message to the discord channel with the name of the winner of the wheel of hamingja.
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)

            logger.info(f"Channel: {channel}")
            logger.info(f"Playername: {playername}")
            logger.info(f"Discord server ID: {channel.discord_server_id}")

            if self.discord_bot.get_guild(int(channel.discord_server_id)):
                discord_server = self.discord_bot.get_guild(int(channel.discord_server_id))

                logger.info(f"Discord server: {discord_server}")
                
                accounts: list[dict[str, any]] = self.twitch_bot.conf_options["APP"]["ACCOUNTS"]
                for account in accounts:
                    if account["name"] == ctx.channel.name.lower():
                        channel_id = account["discord_wheel_of_hamingja_channel_id"]
                        break
                
                playername = playername.strip("@")
                
                if channel_id:
                    logger.info(f"Discord channel ID: {channel_id}")
                    discord_channel = discord_server.get_channel(int(channel_id))
                    await discord_channel.send(f"Congratulations to @{playername} for winning the Wheel of Hamingja! Come and check in to the stream now before the next spin to claim your Tag of Hamingja for your shield. Otherwise it will be lost forever!")
                    await ctx.send(f"The ravens have been sent to collect @{playername} to claim their Tag of Hamingja!")
                else:
                    pass
            else:
                pass
        else:
            pass
    
    @commands.command()
    async def raidbonus(self, ctx: commands.Context, bonuspoints: int) -> None:
        """
        ?raidbonus command

        Add the bonus points to everyone who is checked into the current raid session.
        """
        if await Channel.get_or_none(name=ctx.channel.name):
            channel = await Channel.get(name=ctx.channel.name)
            logging.info(f"Channel exists: {channel}")
            if await Season.active_seasons.all().filter(channel=channel).exists():
                season: Season = await Season.active_seasons.all().filter(channel=channel).first()
                logging.info(f"Active season: {season}")
                if await RaidSession.active_session.all().filter(channel=channel).exists():
                    logging.info("Raid session exists.")
                    raid_session = await RaidSession.active_session.all().filter(channel=channel).first()
                    logging.info(f"Raid session: {raid_session}")
                    checkins = await RaidCheckin.all().filter(session=raid_session)
                    logging.info(f"Checkins: {checkins}")
                    for checkin in checkins:
                        player = await checkin.player
                        if await Points.get_or_none(player=player, season=season, channel=channel):
                            points = await Points.get(player=player, season=season, channel=channel)
                            points.points += bonuspoints
                            await points.save()
                        else:
                            await Points.create(
                                player_id=player.id,
                                season_id=season.id,
                                points=bonuspoints,
                                clan_id=player.clan.id,
                                channel=channel,
                            )
                    await ctx.send(f"Congratulations Raiders! You've ALL earned a bonus {bonuspoints} VP for opening RAID CHESTS on RAID DAY! vander60SKAL")
                else:
                    logging.info("No raid session exists.")
                    await ctx.send("No raid is currently in progress.")
            else:
                logging.info("No active seasons.")
                await ctx.send("No active seasons!")
        else:
            pass

    @commands.command()
    async def skal(self, ctx: commands.Context) -> None:
        """
        ?skal command
        """
        await ctx.send("vander60SKAL vander60SKAL vander60SKAL vander60SKAL vander60SKAL vander60SKAL vander60SKAL vander60SKAL vander60SKAL vander60SKAL vander60SKAL vander60SKAL vander60SKAL vander60SKAL vander60SKAL vander60SKAL vander60SKAL vander60SKAL")
    
    @commands.command()
    async def blades(self, ctx: commands.Context) -> None:
        """
        ?blades command
        """
        await ctx.send("vander60AXE vander60AXE vander60AXE vander60AXE vander60AXE vander60AXE vander60AXE vander60AXE vander60AXE vander60AXE vander60AXE vander60AXE vander60AXE vander60AXE vander60AXE vander60AXE vander60AXE vander60AXE vander60AXE vander60AXE")

    @commands.command()
    async def shields(self, ctx: commands.Context) -> None:
        """
        ?shields command
        """
        await ctx.send("vander60SHIELD vander60SHIELD vander60SHIELD vander60SHIELD vander60SHIELD vander60SHIELD vander60SHIELD vander60SHIELD vander60SHIELD vander60SHIELD vander60SHIELD vander60SHIELD vander60SHIELD vander60SHIELD vander60SHIELD vander60SHIELD vander60SHIELD vander60SHIELD")

    @commands.command()
    async def boats(self, ctx: commands.Context) -> None:
        """
        ?boats command
        """
        await ctx.send("vander60RAIDBOAT vander60RAIDBOAT vander60RAIDBOAT vander60RAIDBOAT vander60RAIDBOAT vander60RAIDBOAT vander60RAIDBOAT vander60RAIDBOAT vander60RAIDBOAT vander60RAIDBOAT vander60RAIDBOAT vander60RAIDBOAT vander60RAIDBOAT vander60RAIDBOAT vander60RAIDBOAT vander60RAIDBOAT")

    @commands.command()
    async def raidshields(self, ctx: commands.Context) -> None:
        """
        ?raidshields command
        """
        await ctx.send("vander60RAIDCHAMP vander60RAIDCHAMP vander60RAIDCHAMP vander60RAIDCHAMP vander60RAIDCHAMP vander60RAIDCHAMP vander60RAIDCHAMP vander60RAIDCHAMP vander60RAIDCHAMP vander60RAIDCHAMP vander60RAIDCHAMP vander60RAIDCHAMP vander60RAIDCHAMP vander60RAIDCHAMP vander60RAIDCHAMP")

def prepare(twitch_bot: commands.Bot, discord_bot: discord_commands.Bot) -> None:
    twitch_bot.add_cog(BomModCommandsCog(twitch_bot, discord_bot))
