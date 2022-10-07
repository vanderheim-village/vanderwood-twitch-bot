from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "season" ADD "name" VARCHAR(255) NOT NULL UNIQUE;
        CREATE UNIQUE INDEX "uid_season_name_22f05f" ON "season" ("name");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_season_name_22f05f";
        ALTER TABLE "season" DROP COLUMN "name";"""
