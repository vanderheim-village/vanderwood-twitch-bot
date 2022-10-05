# Import libraries
import logging
import os
import sys
import traceback
from typing import Any, Dict, List

import yaml
from aiohttp import ClientSession
from aiohttp.web_runner import GracefulExit
from twitchio.ext import commands, eventsub
from tortoise import Tortoise

from app import settings


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

    #@eventsubbot.event()
    #async def event_eventsub_notification_follow(payload: eventsub.ChannelFollowData) -> None:
    #    """
    #    Reacts to receicing a new channel follow event. It will respond in chat thanking the follower and giving them the discord link.
    #    """
    #    print(payload.data.id)

    eventsub_client = eventsub.EventSubClient(
        eventsubbot,
        conf_options["APP"]["SECRET_STRING"],
        conf_options["APP"]["CALLBACK_URL"],
    )

    #async def subscribe_follows(channel_id: int) -> None:
    #    """
    #    Subscribes to new channel follow events.
    #    """
    #    try:
    #        await eventsub_client.subscribe_channel_follows(channel_id)
    #    except twitchio.HTTPException as err:
    #        if err.status == 409:
    #            pass
    #        else:
    #            raise

    bot.loop.create_task(eventsub_client.listen(port=conf_options["APP"]["PORT"]))
    bot.loop.create_task(bot.tinit())
    bot.loop.create_task(bot.connect())
    for channel in conf_options["APP"]["ACCOUNTS"]:
        #eventsubbot.loop.create_task(subscribe_follows(channel["id"]))
        pass
    try:
        bot.loop.run_forever()
        bot.loop.run_until_complete(bot.stop())
    except GracefulExit:
        bot.loop.run_until_complete(bot.stop())
        sys.exit(0)
