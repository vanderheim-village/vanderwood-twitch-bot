from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "spoilsclaim" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "channel_id" INT NOT NULL REFERENCES "channel" ("id") ON DELETE CASCADE,
    "player_id" INT NOT NULL REFERENCES "player" ("id") ON DELETE CASCADE,
    "spoils_session_id" INT NOT NULL REFERENCES "spoilssession" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "spoilsclaim";"""
