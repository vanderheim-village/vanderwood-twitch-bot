# Import libraries
import importlib
import logging
from app.logger import CustomFormatter
# Set up logging

discord_logger = logging.getLogger("discord_bot")
twitch_logger = logging.getLogger("twitch_bot")

log_handler = logging.StreamHandler()
log_handler.setFormatter(CustomFormatter())

logging.basicConfig(level=logging.INFO, handlers=[log_handler])

import os
import random
import sys
import traceback
from typing import Any, Dict, List

import twitchio
import yaml
from aiohttp import ClientSession
from aiohttp.web_runner import GracefulExit
import discord
from discord.ext import commands as discord_commands
from tortoise import Tortoise
from twitchio.ext import commands, eventsub
from tortoise.functions import Count
from twitchio.models import PartialUser

from app import settings
from app.models import EventSubscriptions, Player, Points, Season, Subscriptions, Clan, Channel, GiftedSubsLeaderboard


# Define function to process yaml config file
def process_config_file() -> Any:
    with open("config.yaml", "r") as stream:
        config_options = yaml.safe_load(stream)

    return config_options


class DiscordBot(discord_commands.Bot):
    def __init__(self, *args, **kwargs):
        self.conf_options = kwargs.pop("conf_options")
        super().__init__(*args, **kwargs)
    
    async def on_ready(self) -> None:
        discord_logger.info(f"Logged in as {self.user.name}")
        await self.change_presence(activity=discord.Game(name="/help"))
        self.alert_channel = self.get_channel(self.conf_options["APP"]["DISCORD_ALERT_CHANNEL"])
    
    async def setup_hook(self) -> None:
        for filename in os.listdir("./app/modules/discord_cogs/"):
            if filename.endswith(".py") and not filename.startswith("__init__"):
                try:
                    await discord_bot.load_extension(f"app.modules.discord_cogs.{filename}".strip(".py"))
                    discord_logger.info(f"Loaded extension app.modules.discord_cogs.{filename}.")
                except Exception:
                    discord_logger.error(f"Failed to load extension app.modules.discord_cogs.{filename}.")
                    traceback.print_exc()
    
    async def log_message(self, message: str) -> None:
        await self.alert_channel.send(message)


# Define Bot class
class TwitchBot(commands.Bot):
    def __init__(
        self,
        access_token: str,
        prefix: str,
        initial_channels: List[str],
        conf_options: Dict[str, Any],
        discord_bot: discord_commands.Bot,
    ):
        """
        Tells the Bot class which token it should use, channels to connect to and prefix to use.
        """
        self.conf_options = conf_options
        self.discord_bot = discord_bot
        super().__init__(token=access_token, prefix=prefix, initial_channels=initial_channels)

    async def tinit(self) -> None:
        self.session = ClientSession()
        await Tortoise.init(
            config=settings.TORTOISE,
        )

        await Tortoise.generate_schemas(safe=True)

    async def stop(self) -> None:
        await self.session.close()
        await Tortoise.close_connections()
    
    async def event_message(self, message: twitchio.Message) -> None:
        if message.echo:
            msg: str = message.content
            if msg.startswith("https://clips.twitch.tv"):
                logging.info("Received a clip message event.")
                discord_server = self.discord_bot.get_guild(self.conf_options["APP"]["DISCORD_SERVER_ID"])
                clip_channel = discord_server.get_channel(self.conf_options["APP"]["DISCORD_CLIP_CHANNEL"])
                await clip_channel.send(f"RVNSBOT shared a clip: {msg}")
            else:
                return
        else:
            if await Channel.get_or_none(name=message.channel.name):
                channel = await Channel.get(name=message.channel.name)
                if "msg-id" in message.tags:
                    if message.tags["msg-id"] == "highlighted-message":
                        logging.info("Received a highlighted message event.")
                        await self.discord_bot.log_message("Received a highlighted message event.")
                        if await Player.get_or_none(name=message.author.name.lower(), channel=channel):
                            player = await Player.get(name=message.author.name.lower(), channel=channel)
                            if await Season.active_seasons.all().filter(channel=channel).exists():
                                season = await Season.active_seasons.filter(channel=channel).first()
                                if player.is_enabled() and player.clan:
                                    clan = await player.clan.get()
                                    if await Points.get_or_none(player=player, season=season, channel=channel):
                                        points = await Points.get(player=player, season=season, channel=channel)
                                        points.points += self.conf_options["APP"]["HIGHLIGHTED_MESSAGE_POINTS"]
                                        await points.save()
                                    else:
                                        assert player.clan is not None
                                        await Points.create(
                                            player_id=player.id,
                                            season_id=season.id,
                                            points=self.conf_options["APP"]["HIGHLIGHTED_MESSAGE_POINTS"],
                                            clan_id=clan.id,
                                            chanel=channel,
                                        )
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    msg: str = message.content
                    if msg.startswith("https://clips.twitch.tv"):
                        logging.info("Received a clip message event.")
                        discord_server = self.discord_bot.get_guild(self.conf_options["APP"]["DISCORD_SERVER_ID"])
                        clip_channel = discord_server.get_channel(self.conf_options["APP"]["DISCORD_CLIP_CHANNEL"])
                        await clip_channel.send(f"{message.author.name} shared a clip: {msg}")
            else:
                pass
            twitch_logger.info(f"{message.author.name}: {message.content}")
            await self.handle_commands(message)


if __name__ == "__main__":
    conf_options = process_config_file()
    if conf_options["APP"]["DEBUG"] == True:
        logging.basicConfig(handlers=[log_handler], level=logging.DEBUG)
    elif conf_options["APP"]["DEBUG"] == False:
        logging.basicConfig(handlers=[log_handler], level=logging.INFO)
    channel_names = []
    for channel in conf_options["APP"]["ACCOUNTS"]:
        channel_names.append("#" + channel["name"])
    
    intents = discord.Intents.default()
    intents.guilds = True
    intents.message_content = True

    discord_bot = DiscordBot(
        command_prefix="?",
        conf_options=conf_options,
        intents=intents,
        owner_id=conf_options["APP"]["DISCORD_OWNER_ID"],
    )

    twitch_bot = TwitchBot(
        access_token=conf_options["APP"]["ACCESS_TOKEN"],
        prefix="?",
        initial_channels=channel_names,
        conf_options=conf_options,
        discord_bot=discord_bot,
    )

    for filename in os.listdir("./app/modules/cogs/"):
        if filename.endswith(".py") and not filename.startswith("__init__"):
            try:
                module = importlib.import_module(f"app.modules.cogs.{filename.strip('.py')}")

                if hasattr(module, "prepare"):
                    module.prepare(twitch_bot, discord_bot)
                    twitch_logger.info(f"Loaded extension app.modules.cogs.{filename}.")
            except Exception:
                twitch_logger.error(f"Failed to load extension app.modules.cogs.{filename}.")
                traceback.print_exc()

    twitch_eventsubbot = TwitchBot.from_client_credentials(
        client_id=conf_options["APP"]["CLIENT_ID"],
        client_secret=conf_options["APP"]["CLIENT_SECRET"],
    )

    @twitch_eventsubbot.event()
    async def event_eventsub_notification_subscription(
        payload: eventsub.ChannelSubscribeData,
    ) -> None:
        """
        Reacts to receicing a new channel subscription event.
        """

        logging.info(f"User: {payload.data.user.name}")
        logging.info(f"Tier: {payload.data.tier}")
        logging.info(f"Payload: {payload.data}")

        subscribed_user: PartialUser = payload.data.user
        subscription_tier: int = payload.data.tier
        
        logging.info("Received a new subscription event.")
        if await Channel.get_or_none(name=payload.data.broadcaster.name.lower()):
            logging.info(f"Channel {payload.data.broadcaster.name} exists.")
            channel = await Channel.get(name=payload.data.broadcaster.name.lower())
            match subscription_tier:
                case 1000:
                    points_to_add = conf_options["APP"]["POINTS"]["TIER_1"]
                case 2000:
                    points_to_add = conf_options["APP"]["POINTS"]["TIER_2"]
                case 3000:
                    points_to_add = conf_options["APP"]["POINTS"]["TIER_3"]

            if await Player.get_or_none(name=subscribed_user.name.lower(), channel=channel):
                logging.info(f"Player {subscribed_user.name.lower()} exists.")
                player = await Player.get(name=subscribed_user.name.lower(), channel=channel)
                if await Subscriptions.get_or_none(player=player, channel=channel):
                    subscription = await Subscriptions.get(player=player, channel=channel)
                    subscription.months_subscribed += 1
                    subscription.currently_subscribed = True
                    await subscription.save()
                else:
                    await Subscriptions.create(
                        player=player,
                        months_subscribed=1,
                        currently_subscribed=True,
                        channel=channel,
                    )
                if await Season.active_seasons.all().filter(channel=channel).exists():
                    season = await Season.active_seasons.filter(channel=channel).first()
                    if player.is_enabled() and player.clan:
                        clan = await player.clan.get()
                        if await Points.get_or_none(player=player, season=season, channel=channel):
                            points = await Points.get(player=player, season=season, channel=channel)
                            points.points += points_to_add
                            await points.save()
                        else:
                            assert player.clan is not None
                            await Points.create(
                                player_id=player.id,
                                season_id=season.id,
                                points=points_to_add,
                                clan_id=clan.id,
                                channel=channel,
                            )
                        
                        await twitch_bot.get_channel(payload.data.broadcaster.name).send(
                            f"Hej, @{player.name.lower()}! Welcome to the VANDERWOOD FAMILY! Your clan, the {clan.name.upper()} has gained a new warrior. You can now forge your !shield for WALLHALLA and use ?checkin every live stream to earn ⬣100 VALOR POINTS for you and your clan! Skál! vander60SKAL"
                        )
                    else:
                        "Player is not enabled or does not have a clan"
                        pass
                else:
                    "No active seasons"
                    pass
            else:
                logging.info(f"Player {subscribed_user.name.lower()} does not exist.")
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
                await Player.create(name=subscribed_user.name.lower(), clan_id=new_clan, channel=channel)
                logging.info(f"Created player {subscribed_user.name.lower()}.")
                player = await Player.get(name=subscribed_user.name.lower(), channel=channel)
                if await Subscriptions.get_or_none(player=player, channel=channel):
                    subscription = await Subscriptions.get(player=player, channel=channel)
                    subscription.months_subscribed += 1
                    subscription.currently_subscribed = True
                    await subscription.save()
                else:
                    await Subscriptions.create(
                        player=player,
                        months_subscribed=1,
                        currently_subscribed=True,
                        channel=channel,
                    )
                if await Season.active_seasons.all().filter(channel=channel).exists():
                    season = await Season.active_seasons.filter(channel=channel).first()
                    if player.is_enabled() and player.clan:
                        clan = await player.clan.get()
                        if await Points.get_or_none(player=player, season=season, channel=channel):
                            points = await Points.get(player=player, season=season, channel=channel)
                            points.points += points_to_add
                            await points.save()
                        else:
                            assert player.clan is not None
                            await Points.create(
                                player_id=player.id,
                                season_id=season.id,
                                points=points_to_add,
                                clan_id=clan.id,
                                channel=channel,
                            )
                        
                        await twitch_bot.get_channel(payload.data.broadcaster.name).send(
                            f"Hej, @{player.name.lower()}! Welcome to the VANDERWOOD FAMILY! Your clan, the {clan.name.upper()} has gained a new warrior. You can now forge your !shield for WALLHALLA and use ?checkin every live stream to earn ⬣100 VALOR POINTS for you and your clan! Skál! vander60SKAL"
                        )
                    else:
                        "Player is not enabled or does not have a clan"
                        pass
                else:
                    "No active seasons"
                    pass
        else:
            pass
    
    @twitch_eventsubbot.event()
    async def event_eventsub_notification_subscription_gift(
        payload: eventsub.ChannelSubscriptionGiftData,
    ) -> None:
        """
        Reacts to receiving a new channel subscription gift event.
        """

        logging.info(f"User: {payload.data.user.name}")
        logging.info(f"Tier: {payload.data.tier}")
        logging.info(f"Payload: {payload.data}")


        gift_giver: PartialUser = payload.data.user
        subscription_tier: int = payload.data.tier
        is_anonymous: bool = payload.data.is_anonymous

        logging.info("Received a new subscription gift event.")

        if await Channel.get_or_none(name=payload.data.broadcaster.name.lower()):
            logging.info(f"Channel {payload.data.broadcaster.name} exists.")
            channel = await Channel.get(name=payload.data.broadcaster.name.lower())
            match subscription_tier:
                case 1000:
                    points_to_add = conf_options["APP"]["POINTS"]["TIER_1"]
                case 2000:
                    points_to_add = conf_options["APP"]["POINTS"]["TIER_2"]
                case 3000:
                    points_to_add = conf_options["APP"]["POINTS"]["TIER_3"]
            
            logging.info(f"Points to add: {points_to_add}")

        if is_anonymous:
            logging.info("Gift was anonymous.")
            pass
        else:
            if await Player.get_or_none(name=gift_giver.name.lower(), channel=channel):
                logging.info(f"Player gifter {gift_giver.name.lower()} exists.")
                player = await Player.get(name=gift_giver.name.lower(), channel=channel)
                if await Season.active_seasons.all().filter(channel=channel).exists():
                    season = await Season.active_seasons.filter(channel=channel).first()
                    if player.is_enabled() and player.clan:
                        clan = await player.clan.get()
                        if await Points.get_or_none(player=player, season=season, channel=channel):
                            points = await Points.get(player=player, season=season, channel=channel)
                            points.points += points_to_add
                            await points.save()
                        else:
                            assert player.clan is not None
                            await Points.create(
                                player_id=player.id,
                                season_id=season.id,
                                points=points_to_add,
                                clan_id=clan.id,
                                channel=channel,
                            )
                        
                        if GiftedSubsLeaderboard.all().filter(channel=channel, player=player).exists():
                            gifted_sub = await GiftedSubsLeaderboard.get(channel=channel, player=player)
                            gifted_sub.gifted_subs += 1
                            await gifted_sub.save()
                        else:
                            await GiftedSubsLeaderboard.create(channel=channel, player=player, gifted_subs=1)
                    else:
                        logging.info("Player is not enabled or does not have a clan")
                        pass
                else:
                    logging.info("No active seasons")
                    pass
            else:
                logging.info(f"Player gifter {gift_giver.name.lower()} does not exist.")
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
                await Player.create(name=gift_giver.name.lower(), clan_id=new_clan, channel=channel)
                logging.info(f"Created player {gift_giver.name.lower()}.")
                player = await Player.get(name=gift_giver.name.lower(), channel=channel)
                if await Season.active_seasons.all().filter(channel=channel).exists():
                    season = await Season.active_seasons.filter(channel=channel).first()
                    if player.is_enabled() and player.clan:
                        clan = await player.clan.get()
                        if await Points.get_or_none(player=player, season=season, channel=channel):
                            points = await Points.get(player=player, season=season, channel=channel)
                            points.points += points_to_add
                            await points.save()
                        else:
                            assert player.clan is not None
                            await Points.create(
                                player_id=player.id,
                                season_id=season.id,
                                points=points_to_add,
                                clan_id=clan.id,
                                channel=channel,
                            )
                        
                        if GiftedSubsLeaderboard.all().filter(channel=channel, player=player).exists():
                            gifted_sub = await GiftedSubsLeaderboard.get(channel=channel, player=player)
                            gifted_sub.gifted_subs += 1
                            await gifted_sub.save()
                        else:
                            await GiftedSubsLeaderboard.create(channel=channel, player=player, gifted_subs=1)
                        
                        await twitch_bot.get_channel(payload.data.broadcaster.name).send(
                            f"Hej, @{player.name.lower()}! Welcome to the VANDERWOOD FAMILY! Your clan, the {clan.name.upper()} has gained a new warrior. You can now forge your !shield for WALLHALLA and use ?checkin every live stream to earn ⬣100 VALOR POINTS for you and your clan! Skál! vander60SKAL"
                        )
                    else:
                        logging.info("Player is not enabled or does not have a clan")
                        pass
                else:
                    logging.info("No active seasons")
                    pass

    
    @twitch_eventsubbot.event()
    async def event_eventsub_notification_subscription_message(
        payload: eventsub.ChannelSubscribeData,
    ) -> None:
        """
        Reacts to receicing a new channel subscription event.
        """

        logging.info(f"User: {payload.data.user.name}")
        logging.info(f"Tier: {payload.data.tier}")
        logging.info(f"Payload: {payload.data}")

        subscribed_user: PartialUser = payload.data.user
        subscription_tier: int = payload.data.tier
        
        logging.info("Received a new subscription event.")
        if await Channel.get_or_none(name=payload.data.broadcaster.name.lower()):
            logging.info(f"Channel {payload.data.broadcaster.name} exists.")
            channel = await Channel.get(name=payload.data.broadcaster.name.lower())
            match subscription_tier:
                case 1000:
                    points_to_add = conf_options["APP"]["POINTS"]["TIER_1"]
                case 2000:
                    points_to_add = conf_options["APP"]["POINTS"]["TIER_2"]
                case 3000:
                    points_to_add = conf_options["APP"]["POINTS"]["TIER_3"]

            logging.info(f"Points to add: {points_to_add}")

            if await Player.get_or_none(name=subscribed_user.name.lower(), channel=channel):
                logging.info(f"Player {subscribed_user.name.lower()} exists.")
                player = await Player.get(name=subscribed_user.name.lower(), channel=channel)
                if await Subscriptions.get_or_none(player=player, channel=channel):
                    subscription = await Subscriptions.get(player=player, channel=channel)
                    subscription.months_subscribed += 1
                    subscription.currently_subscribed = True
                    await subscription.save()
                else:
                    await Subscriptions.create(
                        player=player,
                        months_subscribed=1,
                        currently_subscribed=True,
                        channel=channel,
                    )
                if await Season.active_seasons.all().filter(channel=channel).exists():
                    season = await Season.active_seasons.filter(channel=channel).first()
                    if player.is_enabled() and player.clan:
                        clan = await player.clan.get()
                        if await Points.get_or_none(player=player, season=season, channel=channel):
                            points = await Points.get(player=player, season=season, channel=channel)
                            points.points += points_to_add
                            await points.save()
                        else:
                            assert player.clan is not None
                            await Points.create(
                                player_id=player.id,
                                season_id=season.id,
                                points=points_to_add,
                                clan_id=clan.id,
                                channel=channel,
                            )
                    else:
                        "Player is not enabled or does not have a clan"
                        pass
                else:
                    "No active seasons"
                    pass
            else:
                logging.info(f"Player {subscribed_user.name.lower()} does not exist.")
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
                await Player.create(name=subscribed_user.name.lower(), clan_id=new_clan, channel=channel)
                logging.info(f"Created player {subscribed_user.name.lower()}.")
                player = await Player.get(name=subscribed_user.name.lower(), channel=channel)
                if await Subscriptions.get_or_none(player=player, channel=channel):
                    subscription = await Subscriptions.get(player=player, channel=channel)
                    subscription.months_subscribed += 1
                    subscription.currently_subscribed = True
                    await subscription.save()
                else:
                    await Subscriptions.create(
                        player=player,
                        months_subscribed=1,
                        currently_subscribed=True,
                        channel=channel,
                    )
                if await Season.active_seasons.all().filter(channel=channel).exists():
                    season = await Season.active_seasons.filter(channel=channel).first()
                    if player.is_enabled() and player.clan:
                        clan = await player.clan.get()
                        if await Points.get_or_none(player=player, season=season, channel=channel):
                            points = await Points.get(player=player, season=season, channel=channel)
                            points.points += points_to_add
                            await points.save()
                        else:
                            assert player.clan is not None
                            await Points.create(
                                player_id=player.id,
                                season_id=season.id,
                                points=points_to_add,
                                clan_id=clan.id,
                                channel=channel,
                            )
                    else:
                        "Player is not enabled or does not have a clan"
                        pass
                else:
                    "No active seasons"
                    pass
        else:
            pass


    @twitch_eventsubbot.event()
    async def event_eventsub_notification_channel_reward_redeem(
        payload: eventsub.CustomRewardRedemptionAddUpdateData,
    ) -> None:
        """
        Reacts to receiving a new channel points redemption event.
        """
        logging.info(f"Parsed payload: {str(payload.data)}")

        user: PartialUser = payload.data.user
        reward: eventsub.CustomReward = payload.data.reward

        logging.info("Received a new channel points redemption event.")
        if await Channel.get_or_none(name=payload.data.broadcaster.name.lower()):
            logging.info(f"Channel {payload.data.broadcaster.name} exists.")
            channel = await Channel.get(name=payload.data.broadcaster.name.lower())
            if await Player.get_or_none(name=user.name.lower(), channel=channel):
                logging.info(f"Player {user.name.lower()} exists.")
                player = await Player.get(name=user.name.lower(), channel=channel)
                if await Season.active_seasons.all().filter(channel=channel).exists():
                    season = await Season.active_seasons.filter(channel=channel).first()
                    if player.is_enabled() and player.clan:
                        clan = await player.clan.get()
                        if await Points.get_or_none(player=player, season=season, channel=channel):
                            points = await Points.get(player=player, season=season, channel=channel)
                            points.points += reward.cost / 2

                            logging.info(f"Reward cost: {reward.cost}")
                            logging.info(f"Points to add: {reward.cost / 2}")

                            await points.save()
                        else:
                            assert player.clan is not None
                            await Points.create(
                                player_id=player.id,
                                season_id=season.id,
                                points=reward.cost,
                                clan_id=clan.id,
                                channel=channel,
                            )
                        
                        discord_server = discord_bot.get_guild(conf_options["APP"]["DISCORD_SERVER_ID"])
                        discord_channel = discord_server.get_channel(conf_options["APP"]["DISCORD_LOG_CHANNEL"])
                        await discord_channel.send(f"@{user.name.lower()} redeemed a reward: {reward.title}")
                    else:
                        pass
                else:
                    pass
            else:
                logging.info(f"Player {user.name.lower()} does not exist.")
                pass
        else:
            pass
    
    @twitch_eventsubbot.event()
    async def event_eventsub_notification_followV2(
        payload: eventsub.ChannelFollowData,
    ) -> None:
        """
        Reacts to receiving a new channel follow event.
        """
        logging.info(f"User: {payload.data.user.name}")
        logging.info(f"Payload: {payload.data}")

        player: PartialUser = payload.data.user

        logging.info("Received a new follow event.")

        await twitch_bot.get_channel(payload.data.broadcaster.name).send(
            f"Hej @{player.name.lower()}, welcome to VANDERHEIM! Make yourself at home, grab yourself a drink and meet the rest of the VANDERWOOD FAMILY! vander60SKAL"
        )

        
    eventsub_client = eventsub.EventSubClient(
        twitch_eventsubbot,
        conf_options["APP"]["SECRET_STRING"],
        conf_options["APP"]["CALLBACK_URL"],
    )

    async def subscribe_channel_subscription_gifts(channel_id: int, channel_name: str) -> None:
        """
        Subscribes to new channel subscription gift events.
        """
        try:
            if await EventSubscriptions.filter(
                channel_name=channel_name, event_type="channel.subscription.gift"
            ).exists():
                pass
            else:
                await eventsub_client.subscribe_channel_subscription_gifts(channel_id)
                await EventSubscriptions.create(
                    channel_name=channel_name, event_type="channel.subscription.gift", subscribed=True
                )
        except twitchio.HTTPException as err:
            if err.status == 409:
                await EventSubscriptions.create(
                    channel_name=channel_name, event_type="channel.subscription.gift", subscribed=True
                )
            else:
                raise

    async def subscribe_channel_subscriptions(channel_id: int, channel_name: str) -> None:
        """
        Subscribes to new channel subscription events.
        """
        try:
            if await EventSubscriptions.filter(
                channel_name=channel_name, event_type="channel.subscribe"
            ).exists():
                pass
            else:
                await eventsub_client.subscribe_channel_subscriptions(channel_id)
                await EventSubscriptions.create(
                    channel_name=channel_name, event_type="channel.subscribe", subscribed=True
                )
        except twitchio.HTTPException as err:
            if err.status == 409:
                await EventSubscriptions.create(
                    channel_name=channel_name, event_type="channel.subscribe", subscribed=True
                )
            else:
                raise
    
    async def subscribe_channel_follows_v2(channel_id: int, channel_name: str, bot_user_id: str) -> None:
        """
        Subscribes to new channel follow events.
        """
        try:
            if await EventSubscriptions.filter(
                channel_name=channel_name, event_type="channel.follow"
            ).exists():
                pass
            else:
                await eventsub_client.subscribe_channel_follows_v2(channel_id, bot_user_id)
                await EventSubscriptions.create(
                    channel_name=channel_name, event_type="channel.follow", subscribed=True
                )
        except twitchio.HTTPException as err:
            if err.status == 409:
                await EventSubscriptions.create(
                    channel_name=channel_name, event_type="channel.follow", subscribed=True
                )
            else:
                logging.error(err.message)
                logging.error(err.status)
                logging.error(err.reason)
                raise
    
    async def subscribe_channel_subscription_messages(channel_id: int, channel_name: str) -> None:
        """
        Subscribes to channel resubscription messages.
        """
        try:
            if await EventSubscriptions.filter(
                channel_name=channel_name, event_type="channel.subscription.message"
            ).exists():
                pass
            else:
                await eventsub_client.subscribe_channel_subscription_messages(channel_id)
                await EventSubscriptions.create(
                    channel_name=channel_name, event_type="channel.subscription.message", subscribed=True
                )
        except twitchio.HTTPException as err:
            if err.status == 409:
                await EventSubscriptions.create(
                    channel_name=channel_name, event_type="channel.subscription.message", subscribed=True
                )
            else:
                raise

    async def subscribe_channel_points_redeemed(channel_id: int, channel_name: str) -> None:
        """
        Subscribes to new channel points redeemed events.
        """
        try:
            if await EventSubscriptions.filter(
                channel_name=channel_name,
                event_type="channel.channel_points_custom_reward_redemption.add",
            ).exists():
                pass
            else:
                await eventsub_client.subscribe_channel_points_redeemed(channel_id)
                await EventSubscriptions.create(
                    channel_name=channel_name,
                    event_type="channel.channel_points_custom_reward_redemption.add",
                    subscribed=True,
                )
        except twitchio.HTTPException as err:
            if err.status == 409:
                await EventSubscriptions.create(
                    channel_name=channel_name,
                    event_type="channel.channel_points_custom_reward_redemption.add",
                    subscribed=True,
                )
            else:
                raise

    twitch_bot.loop.create_task(eventsub_client.listen(port=conf_options["APP"]["PORT"]))
    twitch_bot.loop.create_task(discord_bot.start(conf_options["APP"]["DISCORD_TOKEN"]))
    twitch_bot.loop.create_task(twitch_bot.tinit())
    twitch_bot.loop.create_task(twitch_bot.connect())
    for channel in conf_options["APP"]["ACCOUNTS"]:
        twitch_eventsubbot.loop.create_task(
            subscribe_channel_subscriptions(channel_id=channel["id"], channel_name=channel["name"])
        )
        twitch_eventsubbot.loop.create_task(
            subscribe_channel_points_redeemed(
                channel_id=channel["id"], channel_name=channel["name"]
            )
        )
        twitch_eventsubbot.loop.create_task(
            subscribe_channel_subscription_messages(
                channel_id=channel["id"], channel_name=channel["name"]
            )
        )
        twitch_eventsubbot.loop.create_task(
            subscribe_channel_subscription_gifts(channel_id=channel["id"], channel_name=channel["name"])
        )
        twitch_eventsubbot.loop.create_task(
            subscribe_channel_follows_v2(channel_id=channel["id"], channel_name=channel["name"], bot_user_id=conf_options["APP"]["BOT_USER_ID"])
        )
        pass
    try:
        twitch_bot.loop.run_forever()
        twitch_bot.loop.run_until_complete(twitch_bot.stop())
    except GracefulExit:
        twitch_bot.loop.run_until_complete(twitch_bot.stop())
        sys.exit(0)
