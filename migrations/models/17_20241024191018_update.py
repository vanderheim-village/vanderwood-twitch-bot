from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "checkin" ADD "new_guid_id" UUID;
        ALTER TABLE "clan" ADD "new_guid_id" UUID;
        ALTER TABLE "clanspoilsclaim" ADD "new_guid_id" UUID;
        ALTER TABLE "clanspoilssession" ADD "new_guid_id" UUID;
        ALTER TABLE "eventsubscriptions" ADD "new_guid_id" UUID;
        ALTER TABLE "followergiveaway" ADD "new_guid_id" UUID;
        ALTER TABLE "followergiveawayentry" ADD "new_guid_id" UUID;
        ALTER TABLE "followergiveawayprize" ADD "new_guid_id" UUID;
        ALTER TABLE "giftedsubsleaderboard" ADD "new_guid_id" UUID;
        ALTER TABLE "player" ADD "new_guid_id" UUID;
        ALTER TABLE "playerwatchtime" ADD "new_guid_id" UUID;
        ALTER TABLE "points" ADD "new_guid_id" UUID;
        ALTER TABLE "raidcheckin" ADD "new_guid_id" UUID;
        ALTER TABLE "raidsession" ADD "new_guid_id" UUID;
        ALTER TABLE "season" ADD "new_guid_id" UUID;
        ALTER TABLE "sentrycheckin" ADD "new_guid_id" UUID;
        ALTER TABLE "sentrysession" ADD "new_guid_id" UUID;
        ALTER TABLE "session" ADD "new_guid_id" UUID;
        ALTER TABLE "spoilsclaim" ADD "new_guid_id" UUID;
        ALTER TABLE "spoilssession" ADD "new_guid_id" UUID;
        ALTER TABLE "subscriptions" ADD "new_guid_id" UUID;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "clan" DROP COLUMN "new_guid_id";
        ALTER TABLE "player" DROP COLUMN "new_guid_id";
        ALTER TABLE "points" DROP COLUMN "new_guid_id";
        ALTER TABLE "season" DROP COLUMN "new_guid_id";
        ALTER TABLE "checkin" DROP COLUMN "new_guid_id";
        ALTER TABLE "session" DROP COLUMN "new_guid_id";
        ALTER TABLE "raidcheckin" DROP COLUMN "new_guid_id";
        ALTER TABLE "raidsession" DROP COLUMN "new_guid_id";
        ALTER TABLE "spoilsclaim" DROP COLUMN "new_guid_id";
        ALTER TABLE "sentrycheckin" DROP COLUMN "new_guid_id";
        ALTER TABLE "sentrysession" DROP COLUMN "new_guid_id";
        ALTER TABLE "spoilssession" DROP COLUMN "new_guid_id";
        ALTER TABLE "subscriptions" DROP COLUMN "new_guid_id";
        ALTER TABLE "clanspoilsclaim" DROP COLUMN "new_guid_id";
        ALTER TABLE "playerwatchtime" DROP COLUMN "new_guid_id";
        ALTER TABLE "followergiveaway" DROP COLUMN "new_guid_id";
        ALTER TABLE "clanspoilssession" DROP COLUMN "new_guid_id";
        ALTER TABLE "eventsubscriptions" DROP COLUMN "new_guid_id";
        ALTER TABLE "followergiveawayentry" DROP COLUMN "new_guid_id";
        ALTER TABLE "followergiveawayprize" DROP COLUMN "new_guid_id";
        ALTER TABLE "giftedsubsleaderboard" DROP COLUMN "new_guid_id";"""
