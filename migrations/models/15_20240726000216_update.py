from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "playerwatchtime" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "watch_time" INT NOT NULL  DEFAULT 0,
    "channel_id" INT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE,
    "player_id" INT NOT NULL REFERENCES "player" ("id") ON DELETE CASCADE,
    "season_id" INT NOT NULL REFERENCES "season" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "playerwatchtime";"""
