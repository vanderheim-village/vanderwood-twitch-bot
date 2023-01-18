from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "channel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "clan" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "tag" VARCHAR(4) NOT NULL,
    "channel_id" INT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "eventsubscriptions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "channel_name" VARCHAR(255) NOT NULL,
    "event_type" VARCHAR(255) NOT NULL,
    "subscribed" BOOL NOT NULL
);
CREATE TABLE IF NOT EXISTS "player" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "enabled" BOOL NOT NULL  DEFAULT True,
    "channel_id" INT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE,
    "clan_id" INT REFERENCES "clan" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "season" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "start_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "end_date" TIMESTAMPTZ,
    "info_end_date" TIMESTAMPTZ,
    "channel_id" INT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "points" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "points" INT NOT NULL  DEFAULT 0,
    "channel_id" INT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE,
    "clan_id" INT NOT NULL REFERENCES "clan" ("id") ON DELETE CASCADE,
    "player_id" INT NOT NULL REFERENCES "player" ("id") ON DELETE CASCADE,
    "season_id" INT NOT NULL REFERENCES "season" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "session" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "start_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "end_time" TIMESTAMPTZ,
    "channel_id" INT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE,
    "season_id" INT NOT NULL REFERENCES "season" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "checkin" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "channel_id" INT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE,
    "player_id" INT NOT NULL REFERENCES "player" ("id") ON DELETE CASCADE,
    "session_id" INT NOT NULL REFERENCES "session" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "subscriptions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "months_subscribed" INT NOT NULL  DEFAULT 1,
    "currently_subscribed" BOOL NOT NULL,
    "channel_id" INT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE,
    "player_id" INT NOT NULL UNIQUE REFERENCES "player" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
