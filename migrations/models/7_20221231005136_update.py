from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "subscriptions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "months_subscribed" INT NOT NULL  DEFAULT 1,
    "currently_subscribed" BOOL NOT NULL,
    "player_id" INT NOT NULL UNIQUE REFERENCES "player" ("id") ON DELETE CASCADE
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "subscriptions";"""
