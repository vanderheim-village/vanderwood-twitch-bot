from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "sentrycheckin" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "channel_id" INT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE,
    "player_id" INT NOT NULL REFERENCES "player" ("id") ON DELETE CASCADE,
    "session_id" INT NOT NULL REFERENCES "sentrysession" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "sentrysession" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "start_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "end_time" TIMESTAMPTZ,
    "channel_id" INT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE,
    "season_id" INT NOT NULL REFERENCES "season" ("id") ON DELETE CASCADE,
    "session_id" INT NOT NULL REFERENCES "session" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "sentrycheckin";
        DROP TABLE IF EXISTS "sentrysession";"""
