from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "clan" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "tag" VARCHAR(4) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "player" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "enabled" BOOL NOT NULL  DEFAULT True,
    "clan_id" INT NOT NULL REFERENCES "clan" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "season" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "start_date" TIMESTAMPTZ NOT NULL,
    "end_date" TIMESTAMPTZ
);
CREATE TABLE IF NOT EXISTS "points" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "points" INT NOT NULL  DEFAULT 0,
    "clan_id" INT NOT NULL REFERENCES "clan" ("id") ON DELETE CASCADE,
    "player_id" INT NOT NULL REFERENCES "player" ("id") ON DELETE CASCADE,
    "season_id" INT NOT NULL REFERENCES "season" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "session" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "start_time" TIMESTAMPTZ NOT NULL,
    "end_time" TIMESTAMPTZ,
    "season_id" INT NOT NULL REFERENCES "season" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "checkin" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "player_id" INT NOT NULL REFERENCES "player" ("id") ON DELETE CASCADE,
    "session_id" INT NOT NULL REFERENCES "session" ("id") ON DELETE CASCADE
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
