from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "channel" ADD "discord_server_id" VARCHAR(255)  UNIQUE;
        CREATE UNIQUE INDEX "uid_channel_discord_730740" ON "channel" ("discord_server_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_channel_discord_730740";
        ALTER TABLE "channel" DROP COLUMN "discord_server_id";"""
