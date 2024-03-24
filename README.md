# Battle of Midgard Twitch & Discord Bot Documentation

The Battle of Midgard Twitch & Discord Bot is a bot that has been built for the [VanderwoodTV](https://www.twitch.tv/vanderwoodtv) Twitch channel.
The bot is built mainly using the [TwitchIO](https://github.com/TwitchIO/TwitchIO), [discord.py](https://github.com/Rapptz/discord.py) and the [tortoise-orm](https://github.com/tortoise/tortoise-orm) libraries.

The bot has been built and coded by [Adam Birds](https://github.com/adambirds/) of [ADB Web Designs](https://adbwebdesigns.co.uk/).

The documentation for the bot has been created using [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

## Commands

The bot has a number of commands that are available to the streamer, moderators, subscribers and normal viewers.

### Streamer Commands
* **[?registerchannel](docs/commands/streamer-commands/registerchannel.md)** - Registers the channel for the Battle of Midgard game.

### Moderator Commands

* **[?createclan](docs/commands/moderator-commands/createclan.md)** - Creates a clan which viewers can join in the Battle of Midgard game.
* **[?add](docs/commands/moderator-commands/add.md)** - Adds a viewer to a clan in the Battle of Midgard game.
* **[?remove](docs/commands/moderator-commands/remove.md)** - Removes a viewer from a clan in the Battle of Midgard game.
* **[?startseason](docs/commands/moderator-commands/startseason.md)** - Starts a new season of the Battle of Midgard game.
* **[?endseason](docs/commands/moderator-commands/endseason.md)** - Ends the current season of the Battle of Midgard game.
* **[?startsession](docs/commands/moderator-commands/startsession.md)** - Starts a new session of the Battle of Midgard game.
* **[?endsession](docs/commands/moderator-commands/endsession.md)** - Ends the current session of the Battle of Midgard game.
* **[?setdate](docs/commands/moderator-commands/setdate.md)** - Sets the end date of the current season of the Battle of Midgard game.
* **[?addvp](docs/commands/moderator-commands/addvp.md)** - Adds valor points to the viewer for the current season of the Battle of Midgard game.
* **[?removevp](docs/commands/moderator-commands/removevp.md)** - Removes valor points from the viewer for the current season of the Battle of Midgard game.
* **[?addrewardlevel](docs/commands/moderator-commands/addrewardlevel.md)** - Adds a reward level to the Battle of Midgard game.
* **[?editrewardlevel](docs/commands/moderator-commands/editrewardlevel.md)** - Edits a reward level in the Battle of Midgard game.
* **[?removerewardlevel](docs/commands/moderator-commands/removerewardlevel.md)** - Removes a reward level from the Battle of Midgard game.
* **[?startraid](docs/commands/moderator-commands/startraid.md)** - Starts a raid in the Battle of Midgard game.
* **[?endraid](docs/commands/moderator-commands/endraid.md)** - Ends a raid in the Battle of Midgard game.
* **[?clip](docs/commands/moderator-commands/clip.md)** - Creates a clip of the current stream.
* **[?lucky](docs/commands/moderator-commands/lucky.md)** - Announces the winner of the Wheel of Hamingja in the discord server.

### Subscriber Commands

* **[?join](docs/commands/subscriber-commands/join.md)** - Joins the Battle of Midgard game and get randomly assigned to a clan.

### Viewer Commands

* **[?rank](docs/commands/viewer-commands/rank.md)** - Displays the Top 10 players in the clan for the current season of the Battle of Midgard game.
* **[?standings](docs/commands/viewer-commands/standings.md)** - Displays the current clan standings for the current season of the Battle of Midgard game.
* **[?overallrank](docs/commands/viewer-commands/overallrank.md)** - Displays the top 10 players across all clans for the current season of the Battle of Midgard game.
* **[?myrank](docs/commands/viewer-commands/myrank.md)** - Displays the current season points, lifetime points, clan rank and overall rank for the viewer.
* **[?dates](docs/commands/viewer-commands/dates.md)** - Displays the start and end dates for the current season of the Battle of Midgard game.
* **[?mvp](docs/commands/viewer-commands/mvp.md)** - Displays the MVP from the previous season of the Battle of Midgard game.
* **[?checkin](docs/commands/viewer-commands/checkin.md)** - Checks the viewer into the current session of the Battle of Midgard game.
* **[?raid](docs/commands/viewer-commands/raid.md)** - Checks the viewer into the current raid of the Battle of Midgard game.
* **[?giftedsubleaderboard](commands/viewer-commands/giftedsubleaderboard.md)** - Displays the top 10 viewers who have gifted the most subs.
* **[?help](docs/commands/viewer-commands/help.md)** - Displays a link to this documentation.