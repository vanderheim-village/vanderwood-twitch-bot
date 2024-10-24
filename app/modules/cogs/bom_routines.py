import datetime
import logging
import random

from discord.ext import commands as discord_commands
from twitchio.ext import commands, routines

from app.models import (
    Channel,
    FollowerGiveaway,
    FollowerGiveawayEntry,
    FollowerGiveawayPrize,
    Player,
    Points,
    Season,
    SentrySession,
    Session,
)

logger = logging.getLogger(__name__)


class BomRoutinesCog(commands.Cog):
    def __init__(self, twitch_bot: commands.Bot, discord_bot: discord_commands.Bot) -> None:
        self.twitch_bot = twitch_bot
        self.discord_bot = discord_bot

    @routines.routine(minutes=30, wait_first=True)
    async def start_sentry_session(self) -> None:
        logger.info("Starting sentry session, if needed.")

        channels = await Channel.all()

        for channel in channels:
            channel_object = await Channel.get(name=channel.name)
            if await Season.active_seasons.all().filter(channel=channel_object).exists():
                season = await Season.active_seasons.get(channel=channel_object)
                if await Session.active_session.all().filter(channel=channel_object).exists():
                    session = await Session.active_session.filter(channel=channel_object).first()
                    if await SentrySession.active_session.filter(
                        channel=channel_object, session=session
                    ).exists():
                        # Sentry session already exists so do nothing
                        pass
                    else:
                        # Sentry session does not exist so create it, with an end time of 5 minutes from now.
                        end_time = datetime.datetime.now(
                            tz=datetime.timezone.utc
                        ) + datetime.timedelta(minutes=5)
                        await SentrySession.create(
                            channel=channel_object,
                            session=session,
                            end_time=end_time,
                            season=season,
                        )
                        message = f"vander60RAIDCHAMP VIKINGS!! vander60RAIDCHAMP We need YOU to keep watch over the WOODLANDS! Use ?sentry to keep VANDERHEIM safe and earn your TAG of ULLR! 🏹👁️"
                        logger.info(f"Sending message to channel {channel_object.name}: {message}")
                        await self.send_twitch_message(channel_object.name, message)
                else:
                    pass
            else:
                pass

    @start_sentry_session.before_routine
    async def before_start_sentry_session(self) -> None:
        await self.twitch_bot.wait_for_ready()

    @routines.routine(seconds=5, wait_first=True)
    async def check_follower_giveaway_winners(self) -> None:
        logger.info("Checking for follower giveaway winners.")

        channels = await Channel.all()

        for channel in channels:
            channel_object = await Channel.get(name=channel.name)
            if await Season.active_seasons.all().filter(channel=channel_object).exists():
                season = await Season.active_seasons.get(channel=channel_object)
                giveaways = await FollowerGiveaway.filter(channel=channel_object, winner=None)
                for giveaway in giveaways:
                    if giveaway.end_time <= datetime.datetime.now(tz=giveaway.end_time.tzinfo):
                        entries = await FollowerGiveawayEntry.filter(giveaway=giveaway)
                        if entries:
                            winner_entry = random.choice(entries)
                            winner = await winner_entry.player
                            giveaway.winner = winner
                            await giveaway.save()
                            prize = random.choice(
                                await FollowerGiveawayPrize.filter(channel=channel_object)
                            )
                            if await Points.filter(
                                player=winner, channel=channel_object, season=season
                            ).exists():
                                points = await Points.get(
                                    player=winner, channel=channel_object, season=season
                                )
                                points.points += prize.vp_reward
                                await points.save()
                            else:
                                await Points.create(
                                    player=winner,
                                    channel=channel_object,
                                    season=season,
                                    points=prize.vp_reward,
                                    clan=winner.clan,
                                )
                            message = f"@{winner.name} has searched @{giveaway.follower} and found: {prize.message} Thank you @{giveaway.follower}, you may now enter VANDERHEIM!"
                            logger.info(
                                f"Sending message to channel {channel_object.name}: {message}"
                            )
                            await self.send_twitch_message(channel_object.name, message)
                        else:
                            await FollowerGiveaway.filter(id=giveaway.id).delete()
                            message = f"{giveaway.follower} is on the loose in VANDERHEIM!"
                            logger.info(
                                f"Sending message to channel {channel_object.name}: {message}"
                            )
                            await self.send_twitch_message(channel_object.name, message)
                    else:
                        pass
            else:
                pass
        else:
            pass

    @check_follower_giveaway_winners.before_routine
    async def before_check_follower_giveaway_winners(self) -> None:
        await self.twitch_bot.wait_for_ready()

    async def send_twitch_message(self, channel_name: str, message: str) -> None:
        channel = self.twitch_bot.get_channel(channel_name)
        if channel:
            logger.info(f"Channel {channel_name} found, sending message: {message}")
            await channel.send(message)
        else:
            logger.warning(f"Channel {channel_name} not found, unable to send message")


def prepare(twitch_bot: commands.Bot, discord_bot: discord_commands.Bot) -> None:
    cog = BomRoutinesCog(twitch_bot, discord_bot)
    twitch_bot.add_cog(cog)
    twitch_bot.check_follower_giveaways = cog.check_follower_giveaway_winners
    twitch_bot.start_sentry_session = cog.start_sentry_session
