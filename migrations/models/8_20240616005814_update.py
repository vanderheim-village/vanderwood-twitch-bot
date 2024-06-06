from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "followergiveaway" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "start_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "end_time" TIMESTAMPTZ NOT NULL,
    "follower" VARCHAR(255) NOT NULL,
    "channel_id" INT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE,
    "winner_id" INT REFERENCES "player" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "followergiveawayentry" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "channel_id" INT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE,
    "giveaway_id" INT NOT NULL REFERENCES "followergiveaway" ("id") ON DELETE CASCADE,
    "player_id" INT NOT NULL REFERENCES "player" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "followergiveawayprize" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "message" TEXT NOT NULL,
    "vp_reward" INT NOT NULL,
    "channel_id" INT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "followergiveaway";
        DROP TABLE IF EXISTS "followergiveawayentry";
        DROP TABLE IF EXISTS "followergiveawayprize";"""
