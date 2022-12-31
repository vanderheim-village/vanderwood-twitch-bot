from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "eventsubscriptions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "channel_name" VARCHAR(255) NOT NULL,
    "event_type" VARCHAR(255) NOT NULL,
    "subscribed" BOOL NOT NULL
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "eventsubscriptions";"""
