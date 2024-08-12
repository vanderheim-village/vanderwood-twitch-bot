# Import libraries
import importlib
import logging
import requests
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
import datetime

from app import settings
from app.models import EventSubscriptions, Player, Points, Season, Subscriptions, Clan, Channel, GiftedSubsLeaderboard, FollowerGiveaway, Session


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
                    module = importlib.import_module(f"app.modules.discord_cogs.{filename.strip('.py')}")

                    if hasattr(module, "setup"):
                        await module.setup(discord_bot,twitch_bot)
                        discord_logger.info(f"Loaded extension app.modules.discord_cogs.{filename}.")
                except Exception:
                    discord_logger.error(f"Failed to load extension app.modules.discord_cogs.{filename}.")
                    traceback.print_exc()



        # for filename in os.listdir("./app/modules/discord_cogs/"):
        #     if filename.endswith(".py") and not filename.startswith("__init__"):
        #         try:
        #             await discord_bot.load_extension(f"app.modules.discord_cogs.{filename}".strip(".py"))
        #             discord_logger.info(f"Loaded extension app.modules.discord_cogs.{filename}.")
        #         except Exception:
        #             discord_logger.error(f"Failed to load extension app.modules.discord_cogs.{filename}.")
        #             traceback.print_exc()
    
    async def log_message(self, message: str) -> None:
        await self.alert_channel.send(message)


# Define Bot class
class TwitchBot(commands.Bot):
    def __init__(
        self,
        access_token: str,
        client_secret: str,
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
        self.refresh_token_url ="https://id.twitch.tv/oauth2/token"
        self.client_id = conf_options["APP"]["CLIENT_ID"]
        self.client_secret = client_secret
        super().__init__(token=access_token, client_secret=client_secret, prefix=prefix, initial_channels=initial_channels)

    async def tinit(self) -> None:
        self.session = ClientSession()
        await Tortoise.init(
            config=settings.TORTOISE,
        )

        await Tortoise.generate_schemas(safe=True)
    
    async def routines_init(self) -> None:
        self.check_follower_giveaways.start()

        channels = await Channel.all()
        for channel in channels:
            if await Session.active_session.filter(channel=channel).exists():
                twitch_logger.info(f"Starting the sentry session routine.")
                self.start_sentry_session.start()
                # Exit the loop after the first channel with an active session is found as we only need to start the routine once.

    async def stop(self) -> None:
        await self.session.close()
        await Tortoise.close_connections()
    
    async def event_token_expired(self) -> None:
        """
        Reacts to the bot's token expiring.
        """
        twitch_logger.info("Token expired.")
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }
        async with self.session.post(self.refresh_token_url, data=data) as response:
            response_data = await response.json()
            self.token = response_data["access_token"]
            self.refresh_token = response_data["refresh_token"]
            twitch_logger.info("Token refreshed.")
        
        ## Save the new token and refresh to the config file
        self.conf_options["APP"]["ACCESS_TOKEN"] = self.token
        self.conf_options["APP"]["REFRESH_TOKEN"] = self.refresh_token
        with open("config.yaml", "w") as stream:
            yaml.dump(self.conf_options, stream)

        twitch_logger.info("Token saved to config file.")

        return self.token
    
    async def event_message(self, message: twitchio.Message) -> None:
        if message.echo:
            msg: str = message.content
            if msg.startswith("https://clips.twitch.tv"):
                if "custom-reward-id" in message.tags:
                    if message.tags["custom-reward-id"] == conf_options["APP"]["BATTLE_CUT_REWARD_ID"]:
                        return
                twitch_logger.info("Received a clip message event.")
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
                        twitch_logger.info("Received a highlighted message event.")
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
                        if "custom-reward-id" in message.tags:
                            if message.tags["custom-reward-id"] == conf_options["APP"]["BATTLE_CUT_REWARD_ID"]:
                                pass
                            else:
                                twitch_logger.info("Received a clip message event.")
                                discord_server = self.discord_bot.get_guild(self.conf_options["APP"]["DISCORD_SERVER_ID"])
                                clip_channel = discord_server.get_channel(self.conf_options["APP"]["DISCORD_CLIP_CHANNEL"])
                                await clip_channel.send(f"{message.author.name} shared a clip: {msg}")
                        else:
                            twitch_logger.info("Received a clip message event.")
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
    
    data = {
        "client_id": conf_options["APP"]["CLIENT_ID"],
        "client_secret": conf_options["APP"]["CLIENT_SECRET"],
        "grant_type": "refresh_token",
        "refresh_token": conf_options["APP"]["REFRESH_TOKEN"],
    }
    response = requests.post("https://id.twitch.tv/oauth2/token", data=data)
    response_data = response.json()
    conf_options["APP"]["ACCESS_TOKEN"] = response_data["access_token"]
    conf_options["APP"]["REFRESH_TOKEN"] = response_data["refresh_token"]

    with open("config.yaml", "w") as stream:
        yaml.dump(conf_options, stream)
       
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
        client_secret=conf_options["APP"]["CLIENT_SECRET"],
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

        twitch_logger.info(f"User: {payload.data.user.name}")
        twitch_logger.info(f"Tier: {payload.data.tier}")
        twitch_logger.info(f"Payload: {payload.data}")

        subscribed_user: PartialUser = payload.data.user
        subscription_tier: int = payload.data.tier
        
        twitch_logger.info("Received a new subscription event.")
        if await Channel.get_or_none(name=payload.data.broadcaster.name.lower()):
            twitch_logger.info(f"Channel {payload.data.broadcaster.name} exists.")
            channel = await Channel.get(name=payload.data.broadcaster.name.lower())
            match subscription_tier:
                case 1000:
                    points_to_add = conf_options["APP"]["POINTS"]["TIER_1"]
                case 2000:
                    points_to_add = conf_options["APP"]["POINTS"]["TIER_2"]
                case 3000:
                    points_to_add = conf_options["APP"]["POINTS"]["TIER_3"]

            if await Player.get_or_none(name=subscribed_user.name.lower(), channel=channel):
                twitch_logger.info(f"Player {subscribed_user.name.lower()} exists.")
                player = await Player.get(name=subscribed_user.name.lower(), channel=channel)
                if await Subscriptions.get_or_none(player=player, channel=channel):
                    subscription = await Subscriptions.get(player=player, channel=channel)
                    subscription.months_subscribed += 1
                    subscription.currently_subscribed = True
                    await subscription.save()
                else:
                    subscription = await Subscriptions.create(
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
                        
                        discord_server = discord_bot.get_guild(conf_options["APP"]["DISCORD_SERVER_ID"])
                        discord_channel = discord_server.get_channel(conf_options["APP"]["DISCORD_SUBS_LOG_CHANNEL"])
                        await discord_channel.send(f"@{player.name.lower()} has subscribed to {channel.name} for {subscription.months_subscribed} months.")

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
                twitch_logger.info(f"Player {subscribed_user.name.lower()} does not exist.")
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
                twitch_logger.info(f"Created player {subscribed_user.name.lower()}.")
                player = await Player.get(name=subscribed_user.name.lower(), channel=channel)
                if await Subscriptions.get_or_none(player=player, channel=channel):
                    subscription = await Subscriptions.get(player=player, channel=channel)
                    subscription.months_subscribed += 1
                    subscription.currently_subscribed = True
                    await subscription.save()
                else:
                    subscription = await Subscriptions.create(
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
                        
                        discord_server = discord_bot.get_guild(conf_options["APP"]["DISCORD_SERVER_ID"])
                        discord_channel = discord_server.get_channel(conf_options["APP"]["DISCORD_SUBS_LOG_CHANNEL"])
                        await discord_channel.send(f"@{player.name.lower()} has subscribed to {channel.name} for {subscription.months_subscribed} months.")
                        
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

        twitch_logger.info(f"User: {payload.data.user.name}")
        twitch_logger.info(f"Tier: {payload.data.tier}")
        twitch_logger.info(f"Total gifts: {payload.data.total}")
        twitch_logger.info(f"Payload: {payload.data}")


        gift_giver: PartialUser = payload.data.user
        subscription_tier: int = payload.data.tier
        is_anonymous: bool = payload.data.is_anonymous

        twitch_logger.info("Received a new subscription gift event.")

        if await Channel.get_or_none(name=payload.data.broadcaster.name.lower()):
            twitch_logger.info(f"Channel {payload.data.broadcaster.name} exists.")
            channel = await Channel.get(name=payload.data.broadcaster.name.lower())
            match subscription_tier:
                case 1000:
                    points_to_add = (conf_options["APP"]["POINTS"]["TIER_1"] * payload.data.total) / 2
                case 2000:
                    points_to_add = (conf_options["APP"]["POINTS"]["TIER_2"] * payload.data.total) / 2
                case 3000:
                    points_to_add = (conf_options["APP"]["POINTS"]["TIER_3"] * payload.data.total) / 2
            
            twitch_logger.info(f"Points to add: {points_to_add}")

        if is_anonymous:
            twitch_logger.info("Gift was anonymous.")
            pass
        else:
            if await Player.get_or_none(name=gift_giver.name.lower(), channel=channel):
                twitch_logger.info(f"Player gifter {gift_giver.name.lower()} exists.")
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
                        
                        if await GiftedSubsLeaderboard.get_or_none(channel=channel, player=player):
                            gifted_sub = await GiftedSubsLeaderboard.get(channel=channel, player=player)
                            gifted_sub.gifted_subs += payload.data.total
                            await gifted_sub.save()
                        else:
                            await GiftedSubsLeaderboard.create(channel=channel, player=player, gifted_subs=1)
                        

                        discord_server = discord_bot.get_guild(conf_options["APP"]["DISCORD_SERVER_ID"])
                        discord_channel = discord_server.get_channel(conf_options["APP"]["DISCORD_SUBS_LOG_CHANNEL"])
                        await discord_channel.send(f"@{player.name.lower()} has gifted {payload.data.total} subs to {channel.name}.")
                    else:
                        twitch_logger.info("Player is not enabled or does not have a clan")
                        pass
                else:
                    twitch_logger.info("No active seasons")
                    pass
            else:
                twitch_logger.info(f"Player gifter {gift_giver.name.lower()} does not exist.")
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
                twitch_logger.info(f"Created player {gift_giver.name.lower()}.")
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
                        
                        discord_server = discord_bot.get_guild(conf_options["APP"]["DISCORD_SERVER_ID"])
                        discord_channel = discord_server.get_channel(conf_options["APP"]["DISCORD_SUBS_LOG_CHANNEL"])
                        await discord_channel.send(f"@{player.name.lower()} has gifted {payload.data.total} subs to {channel.name}.")

                        await twitch_bot.get_channel(payload.data.broadcaster.name).send(
                            f"Hej, @{player.name.lower()}! Welcome to the VANDERWOOD FAMILY! Your clan, the {clan.name.upper()} has gained a new warrior. You can now forge your !shield for WALLHALLA and use ?checkin every live stream to earn ⬣100 VALOR POINTS for you and your clan! Skál! vander60SKAL"
                        )
                    else:
                        twitch_logger.info("Player is not enabled or does not have a clan")
                        pass
                else:
                    twitch_logger.info("No active seasons")
                    pass

    
    @twitch_eventsubbot.event()
    async def event_eventsub_notification_subscription_message(
        payload: eventsub.ChannelSubscribeData,
    ) -> None:
        """
        Reacts to receicing a new channel subscription event.
        """

        twitch_logger.info(f"User: {payload.data.user.name}")
        twitch_logger.info(f"Tier: {payload.data.tier}")
        twitch_logger.info(f"Payload: {payload.data}")

        subscribed_user: PartialUser = payload.data.user
        subscription_tier: int = payload.data.tier
        
        twitch_logger.info("Received a new subscription event.")
        if await Channel.get_or_none(name=payload.data.broadcaster.name.lower()):
            twitch_logger.info(f"Channel {payload.data.broadcaster.name} exists.")
            channel = await Channel.get(name=payload.data.broadcaster.name.lower())
            match subscription_tier:
                case 1000:
                    points_to_add = conf_options["APP"]["POINTS"]["TIER_1"]
                case 2000:
                    points_to_add = conf_options["APP"]["POINTS"]["TIER_2"]
                case 3000:
                    points_to_add = conf_options["APP"]["POINTS"]["TIER_3"]

            twitch_logger.info(f"Points to add: {points_to_add}")

            if await Player.get_or_none(name=subscribed_user.name.lower(), channel=channel):
                twitch_logger.info(f"Player {subscribed_user.name.lower()} exists.")
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
                        

                        discord_server = discord_bot.get_guild(conf_options["APP"]["DISCORD_SERVER_ID"])
                        discord_channel = discord_server.get_channel(conf_options["APP"]["DISCORD_SUBS_LOG_CHANNEL"])
                        await discord_channel.send(f"@{player.name.lower()} has subscribed to {channel.name} for {subscription.months_subscribed} months.")
                    else:
                        "Player is not enabled or does not have a clan"
                        pass
                else:
                    "No active seasons"
                    pass
            else:
                twitch_logger.info(f"Player {subscribed_user.name.lower()} does not exist.")
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
                twitch_logger.info(f"Created player {subscribed_user.name.lower()}.")
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
                        
                        discord_server = discord_bot.get_guild(conf_options["APP"]["DISCORD_SERVER_ID"])
                        discord_channel = discord_server.get_channel(conf_options["APP"]["DISCORD_SUBS_LOG_CHANNEL"])
                        await discord_channel.send(f"@{player.name.lower()} has subscribed to {channel.name} for {subscription.months_subscribed} months.")
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
        twitch_logger.info(f"Parsed payload: {str(payload.data)}")

        user: PartialUser = payload.data.user
        reward: eventsub.CustomReward = payload.data.reward
        user_input: str = payload.data.input

        twitch_logger.info(f"User: {user.name}")
        twitch_logger.info(f"Reward: {reward.title}")
        twitch_logger.info(f"Reward ID: {reward.id}")
        twitch_logger.info(f"User input: {user_input}")

        twitch_logger.info("Received a new channel points redemption event.")
        if await Channel.get_or_none(name=payload.data.broadcaster.name.lower()):
            twitch_logger.info(f"Channel {payload.data.broadcaster.name} exists.")
            channel = await Channel.get(name=payload.data.broadcaster.name.lower())
            if await Player.get_or_none(name=user.name.lower(), channel=channel):
                twitch_logger.info(f"Player {user.name.lower()} exists.")
                player = await Player.get(name=user.name.lower(), channel=channel)
                if await Season.active_seasons.all().filter(channel=channel).exists():
                    season = await Season.active_seasons.filter(channel=channel).first()
                    if player.is_enabled() and player.clan:
                        clan = await player.clan.get()
                        if await Points.get_or_none(player=player, season=season, channel=channel):
                            points = await Points.get(player=player, season=season, channel=channel)
                            points.points += reward.cost / 2

                            twitch_logger.info(f"Reward cost: {reward.cost}")
                            twitch_logger.info(f"Points to add: {reward.cost / 2}")

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

                        if reward.id == conf_options["APP"]["BATTLE_CUT_REWARD_ID"]:
                            battle_cut_discord_channel = discord_server.get_channel(conf_options["APP"]["DISCORD_BATTLE_CUT_LOG_CHANNEL"])
                            await battle_cut_discord_channel.send(f"@{user.name.lower()} has redeemed a battle cut reward, with the following clip: {user_input}")
                    else:
                        pass
                else:
                    pass
            else:
                twitch_logger.info(f"Player {user.name.lower()} does not exist.")
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
        twitch_logger.info(f"User: {payload.data.user.name}")
        twitch_logger.info(f"Payload: {payload.data}")

        player: PartialUser = payload.data.user

        twitch_logger.info("Received a new follow event.")

        ## Launch a giveaway for the new follower, the end time should be 30 seconds from now.
        if await Channel.get_or_none(name=payload.data.broadcaster.name.lower()):
            twitch_logger.info(f"Channel {payload.data.broadcaster.name} exists.")
            channel = await Channel.get(name=payload.data.broadcaster.name.lower())
            # We need to check if a giveaway exists for the new follower (they may have unfollowed and refollowed), so we need to delete the old giveaway and create a new one.
            if await FollowerGiveaway.get_or_none(channel=channel, follower=player.name.lower()):
                await FollowerGiveaway.get(channel=channel, follower=player.name.lower()).delete()
            await FollowerGiveaway.create(channel=channel, end_time=datetime.datetime.now() + datetime.timedelta(seconds=30), follower=player.name.lower())
        else:
            pass

        await twitch_bot.get_channel(payload.data.broadcaster.name).send(
            f"🌲🌲🌲Who goes there!!? 👀 A weary traveller has emerged from the WOODLANDS. I need someone to ?search @{player.name} now before they enter VANDERHEIM!🌲🌲🌲"
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
                    channel_name=channel_name, event_type="channel.subscription.gift", subscribed=True, channel_id=channel_id
                )
        except twitchio.HTTPException as err:
            if err.status == 409:
                await EventSubscriptions.create(
                    channel_name=channel_name, event_type="channel.subscription.gift", subscribed=True, channel_id=channel_id
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
                    channel_name=channel_name, event_type="channel.subscribe", subscribed=True, channel_id=channel_id
                )
        except twitchio.HTTPException as err:
            if err.status == 409:
                await EventSubscriptions.create(
                    channel_name=channel_name, event_type="channel.subscribe", subscribed=True, channel_id=channel_id
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
                    channel_name=channel_name, event_type="channel.follow", subscribed=True, channel_id=channel_id
                )
        except twitchio.HTTPException as err:
            if err.status == 409:
                await EventSubscriptions.create(
                    channel_name=channel_name, event_type="channel.follow", subscribed=True, channel_id=channel_id
                )
            else:
                twitch_logger.error(err.message)
                twitch_logger.error(err.status)
                twitch_logger.error(err.reason)
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
                    channel_name=channel_name, event_type="channel.subscription.message", subscribed=True, channel_id=channel_id
                )
        except twitchio.HTTPException as err:
            if err.status == 409:
                await EventSubscriptions.create(
                    channel_name=channel_name, event_type="channel.subscription.message", subscribed=True, channel_id=channel_id
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
                    channel_id=channel_id,
                    channel_name=channel_name,
                    event_type="channel.channel_points_custom_reward_redemption.add",
                    subscribed=True,
                )
        except twitchio.HTTPException as err:
            if err.status == 409:
                await EventSubscriptions.create(
                    channel_name=channel_name,
                    channel_id=channel_id,
                    event_type="channel.channel_points_custom_reward_redemption.add",
                    subscribed=True,
                )
            else:
                raise
    
    async def get_eventsub_subscriptions() -> None:
        """
        Gets all active eventsub subscriptions.
        """
        subscriptions = await eventsub_client.get_subscriptions()

        for subscription in subscriptions:
            twitch_logger.info(f"subscription Type: {subscription.type}, Status: {subscription.status}, Transport: {subscription.transport}, Transport Method: {subscription.transport_method}, Subscription ID: {subscription.id}, Subscription Cost: {subscription.cost}")
        
        # We need to check if the subscriptions returned match the ones in the database, if one in the database is not in the subscriptions, we need to delete the database entry and then resubscribe.
        for subscription in await EventSubscriptions.all():
            if subscription.event_type == "channel.subscribe":
                if not any(
                    sub.type == "channel.subscribe" and sub.status == "enabled"
                    for sub in subscriptions
                ):
                    await EventSubscriptions.filter(event_type="channel.subscribe").delete()
                    await subscribe_channel_subscriptions(subscription.channel_id, subscription.channel_name)
            elif subscription.event_type == "channel.subscription.gift":
                if not any(
                    sub.type == "channel.subscription.gift" and sub.status == "enabled"
                    for sub in subscriptions
                ):
                    await EventSubscriptions.filter(event_type="channel.subscription.gift").delete()
                    await subscribe_channel_subscription_gifts(subscription.channel_id, subscription.channel_name)
            elif subscription.event_type == "channel.subscription.message":
                if not any(
                    sub.type == "channel.subscription.message" and sub.status == "enabled"
                    for sub in subscriptions
                ):
                    await EventSubscriptions.filter(event_type="channel.subscription.message").delete()
                    await subscribe_channel_subscription_messages(subscription.channel_id, subscription.channel_name)
            elif subscription.event_type == "channel.channel_points_custom_reward_redemption.add":
                if not any(
                    sub.type == "channel.channel_points_custom_reward_redemption.add" and sub.status == "enabled"
                    for sub in subscriptions
                ):
                    await EventSubscriptions.filter(event_type="channel.channel_points_custom_reward_redemption.add").delete()
                    await subscribe_channel_points_redeemed(subscription.channel_id, subscription.channel_name)
            elif subscription.event_type == "channel.follow":
                if not any(
                    sub.type == "channel.follow" and sub.status == "enabled"
                    for sub in subscriptions
                ):
                    channel = await Channel.get(name=subscription.channel_name)
                    await EventSubscriptions.filter(event_type="channel.follow").delete()
                    await subscribe_channel_follows_v2(channel_name=subscription.channel_name, bot_user_id=conf_options["APP"]["BOT_USER_ID"], channel_id=channel.twitch_channel_id)
            else:
                pass

    twitch_bot.loop.create_task(eventsub_client.listen(port=conf_options["APP"]["PORT"]))
    twitch_bot.loop.create_task(discord_bot.start(conf_options["APP"]["DISCORD_TOKEN"]))
    twitch_bot.loop.create_task(twitch_bot.tinit())
    twitch_bot.loop.create_task(twitch_bot.connect())
    twitch_bot.loop.create_task(twitch_bot.routines_init())

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

        twitch_eventsubbot.loop.create_task(get_eventsub_subscriptions())
    try:
        twitch_bot.loop.run_forever()
        twitch_bot.loop.run_until_complete(twitch_bot.stop())
    except GracefulExit:
        twitch_bot.loop.run_until_complete(twitch_bot.stop())
        sys.exit(0)
