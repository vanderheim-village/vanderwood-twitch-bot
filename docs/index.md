---
title: Getting Started
summary: Getting started with the Battle of Midgard Twitch Bot.
---

# Battle of Midgard Twitch Bot Documentation

The Battle of Midgard Twitch Bot is a bot that has been built for the [VanderwoodTV](https://www.twitch.tv/vanderwoodtv) Twitch channel.
The bot is built mainly using the [TwitchIO](https://github.com/TwitchIO/TwitchIO) and the [tortoise-orm](https://github.com/tortoise/tortoise-orm) libraries.

The bot has been built and coded by [Adam Birds](https://github.com/adambirds/) of [ADB Web Designs](https://adbwebdesigns.co.uk/).

The documentation for the bot has been created using [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

## Commands

The bot has a number of commands that are available to the streamer, moderators, subscribers and normal viewers.

### Streamer Commands
* **[?registerchannel](commands/streamer-commands/registerchannel.md)** - Registers the channel for the Battle of Midgard game.

### Moderator Commands

* **[?createclan](commands/moderator-commands/createclan.md)** - Creates a clan which viewers can join in the Battle of Midgard game.
* **[?add](commands/moderator-commands/add.md)** - Adds a viewer to a clan in the Battle of Midgard game.
* **[?remove](commands/moderator-commands/remove.md)** - Removes a viewer from a clan in the Battle of Midgard game.
* **[?startseason](commands/moderator-commands/startseason.md)** - Starts a new season of the Battle of Midgard game.
* **[?endseason](commands/moderator-commands/endseason.md)** - Ends the current season of the Battle of Midgard game.
* **[?startsession](commands/moderator-commands/startsession.md)** - Starts a new session of the Battle of Midgard game.
* **[?endsession](commands/moderator-commands/endsession.md)** - Ends the current session of the Battle of Midgard game.
* **[?setdate](commands/moderator-commands/setdate.md)** - Sets the end date of the current season of the Battle of Midgard game.
* **[?addvp](commands/moderator-commands/addvp.md)** - Adds valor points to the viewer for the current season of the Battle of Midgard game.
* **[?removevp](commands/moderator-commands/removevp.md)** - Removes valor points from the viewer for the current season of the Battle of Midgard game.
* **[?addrewardlevel](commands/moderator-commands/addrewardlevel.md)** - Adds a reward level to the Battle of Midgard game.
* **[?editrewardlevel](commands/moderator-commands/editrewardlevel.md)** - Edits a reward level in the Battle of Midgard game.
* **[?removerewardlevel](commands/moderator-commands/removerewardlevel.md)** - Removes a reward level from the Battle of Midgard game.
* **[?startraid](commands/moderator-commands/startraid.md)** - Starts a raid in the Battle of Midgard game.
* **[?endraid](commands/moderator-commands/endraid.md)** - Ends a raid in the Battle of Midgard game.
* **[?clip](commands/moderator-commands/clip.md)** - Creates a clip of the current stream.

### Subscriber Commands

* **[?join](commands/subscriber-commands/join.md)** - Joins the Battle of Midgard game and get randomly assigned to a clan.

### Viewer Commands

* **[?rank](commands/viewer-commands/rank.md)** - Displays the Top 10 players in the clan for the current season of the Battle of Midgard game.
* **[?standings](commands/viewer-commands/standings.md)** - Displays the current clan standings for the current season of the Battle of Midgard game.
* **[?overallrank](commands/viewer-commands/overallrank.md)** - Displays the top 10 players across all clans for the current season of the Battle of Midgard game.
* **[?myrank](commands/viewer-commands/myrank.md)** - Displays the current season points, lifetime points, clan rank and overall rank for the viewer.
* **[?dates](commands/viewer-commands/dates.md)** - Displays the start and end dates for the current season of the Battle of Midgard game.
* **[?mvp](commands/viewer-commands/mvp.md)** - Displays the MVP from the previous season of the Battle of Midgard game.
* **[?checkin](commands/viewer-commands/checkin.md)** - Checks the viewer into the current session of the Battle of Midgard game.
* **[?raid](commands/viewer-commands/raid.md)** - Checks the viewer into the current raid of the Battle of Midgard game.
* **[?help](commands/viewer-commands/help.md)** - Displays a link to this documentation.
