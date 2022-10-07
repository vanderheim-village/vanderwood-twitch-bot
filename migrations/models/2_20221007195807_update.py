from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "season" ALTER COLUMN "start_date" TYPE TIMESTAMPTZ USING "start_date"::TIMESTAMPTZ;
        ALTER TABLE "season" ALTER COLUMN "start_date" TYPE TIMESTAMPTZ USING "start_date"::TIMESTAMPTZ;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "season" ALTER COLUMN "start_date" TYPE TIMESTAMPTZ USING "start_date"::TIMESTAMPTZ;
        ALTER TABLE "season" ALTER COLUMN "start_date" TYPE TIMESTAMPTZ USING "start_date"::TIMESTAMPTZ;"""
