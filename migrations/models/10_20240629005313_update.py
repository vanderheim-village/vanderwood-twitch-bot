from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "spoilssession" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "start_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "end_time" TIMESTAMPTZ,
    "points_reward" INT NOT NULL  DEFAULT 0,
    "channel_id" INT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE,
    "season_id" INT NOT NULL REFERENCES "season" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "spoilssession";"""
