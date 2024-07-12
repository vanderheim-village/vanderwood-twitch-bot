from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "clan" ADD "twitch_emoji_name" VARCHAR(255);
        CREATE TABLE IF NOT EXISTS "clanspoilssession" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "start_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "end_time" TIMESTAMPTZ,
    "points_reward" INT NOT NULL  DEFAULT 0,
    "channel_id" INT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE,
    "clan_id" INT NOT NULL REFERENCES "clan" ("id") ON DELETE CASCADE,
    "season_id" INT NOT NULL REFERENCES "season" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "clan" DROP COLUMN "twitch_emoji_name";
        DROP TABLE IF EXISTS "clanspoilssession";"""
