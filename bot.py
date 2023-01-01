# Import libraries
import logging
import os
import sys
import traceback
from typing import Any, Dict, List

import twitchio
import yaml
from aiohttp import ClientSession
from aiohttp.web_runner import GracefulExit
from tortoise import Tortoise
from twitchio.ext import commands, eventsub
from twitchio.models import PartialUser

from app import settings
from app.models import EventSubscriptions, Player, Points, Season, Subscriptions


# Define function to process yaml config file
def process_config_file() -> Any:
    with open("config.yaml", "r") as stream:
        config_options = yaml.safe_load(stream)

    return config_options


# Define Bot class
class Bot(commands.Bot):
    def __init__(
        self,
        access_token: str,
        prefix: str,
        initial_channels: List[str],
        conf_options: Dict[str, Any],
    ):
        """
        Tells the Bot class which token it should use, channels to connect to and prefix to use.
        """
        self.conf_options = conf_options
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


if __name__ == "__main__":
    conf_options = process_config_file()
    if conf_options["APP"]["DEBUG"] == True:
        logging.basicConfig(level=logging.DEBUG)
    channel_names = []
    for channel in conf_options["APP"]["ACCOUNTS"]:
        channel_names.append("#" + channel["name"])
    bot = Bot(
        access_token=conf_options["APP"]["ACCESS_TOKEN"],
        prefix="!",
        initial_channels=channel_names,
        conf_options=conf_options,
    )

    for filename in os.listdir("./app/modules/cogs/"):
        if filename.endswith(".py"):
            try:
                bot.load_module(f"app.modules.cogs.{filename.strip('.py')}")
            except Exception:
                print(f"Failed to load extension modules.cogs.{filename}.", file=sys.stderr)
                traceback.print_exc()

    eventsubbot = Bot.from_client_credentials(
        client_id=conf_options["APP"]["CLIENT_ID"],
        client_secret=conf_options["APP"]["CLIENT_SECRET"],
    )

    @eventsubbot.event()
    async def event_eventsub_notification_subscription(
        payload: eventsub.ChannelSubscribeData,
    ) -> None:
        """
        Reacts to receicing a new channel subscription event.
        """
        subscribed_user = payload.user
        subscription_tier = payload.tier

        match subscription_tier:
            case 1:
                points_to_add = conf_options["APP"]["POINTS"]["TIER_1"]
            case 2:
                points_to_add = conf_options["APP"]["POINTS"]["TIER_2"]
            case 3:
                points_to_add = conf_options["APP"]["POINTS"]["TIER_3"]

        if await Player.get_or_none(name=subscribed_user.name):
            player = await Player.get(name=subscribed_user.name)
            if await Subscriptions.get_or_none(player=player):
                subscription = await Subscriptions.get(player=player)
                subscription.months_subscribed += 1
                subscription.currently_subscribed = True
                await subscription.save()
            else:
                await Subscriptions.create(
                    player=player,
                    months_subscribed=1,
                    currently_subscribed=True,
                )
            if await Season.active_seasons.all().exists():
                season = await Season.active_seasons.first()
                if player.is_enabled() and player.clan:
                    clan = await player.clan.get()
                    if await Points.get_or_none(player=player, season=season):
                        points = await Points.get(player=player, season=season)
                        points.points += points_to_add
                        await points.save()
                    else:
                        assert player.clan is not None
                        await Points.create(
                            player_id=player.id,
                            season_id=season.id,
                            points=points_to_add,
                            clan_id=clan.id,
                        )
                else:
                    pass
            else:
                pass
        else:
            pass

    @eventsubbot.event()
    async def event_eventsub_notification_channel_reward_redeem(
        payload: eventsub.CustomRewardRedemptionAddUpdateData,
    ) -> None:
        """
        Reacts to receiving a new channel points redemption event.
        """
        user: PartialUser = payload.data.user
        reward: eventsub.CustomReward = payload.data.reward

        if await Player.get_or_none(name=user.name.lower()):
            player = await Player.get(name=user.name.lower())
            if await Season.active_seasons.all().exists():
                season = await Season.active_seasons.first()
                if player.is_enabled() and player.clan:
                    clan = await player.clan.get()
                    if await Points.get_or_none(player=player, season=season):
                        points = await Points.get(player=player, season=season)
                        points.points += reward.cost
                        await points.save()
                    else:
                        assert player.clan is not None
                        await Points.create(
                            player_id=player.id,
                            season_id=season.id,
                            points=reward.cost,
                            clan_id=clan.id,
                        )
                else:
                    pass
            else:
                pass
        else:
            pass

    eventsub_client = eventsub.EventSubClient(
        eventsubbot,
        conf_options["APP"]["SECRET_STRING"],
        conf_options["APP"]["CALLBACK_URL"],
    )

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

    bot.loop.create_task(eventsub_client.listen(port=conf_options["APP"]["PORT"]))
    bot.loop.create_task(bot.tinit())
    bot.loop.create_task(bot.connect())
    for channel in conf_options["APP"]["ACCOUNTS"]:
        eventsubbot.loop.create_task(
            subscribe_channel_subscriptions(channel_id=channel["id"], channel_name=channel["name"])
        )
        eventsubbot.loop.create_task(
            subscribe_channel_points_redeemed(
                channel_id=channel["id"], channel_name=channel["name"]
            )
        )
        pass
    try:
        bot.loop.run_forever()
        bot.loop.run_until_complete(bot.stop())
    except GracefulExit:
        bot.loop.run_until_complete(bot.stop())
        sys.exit(0)
