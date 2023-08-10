from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "rewardlevel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "level" INT NOT NULL UNIQUE,
    "reward" VARCHAR(255) NOT NULL,
    "channel_id" INT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "rewardlevel";"""
