from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "channel" ADD "twitch_channel_id" VARCHAR(255)  UNIQUE;
        CREATE UNIQUE INDEX "uid_channel_twitch__9de758" ON "channel" ("twitch_channel_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_channel_twitch__9de758";
        ALTER TABLE "channel" DROP COLUMN "twitch_channel_id";"""
