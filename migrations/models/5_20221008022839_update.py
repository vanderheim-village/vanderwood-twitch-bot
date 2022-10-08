from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "session" ALTER COLUMN "start_time" TYPE TIMESTAMPTZ USING "start_time"::TIMESTAMPTZ;
        ALTER TABLE "session" ALTER COLUMN "start_time" TYPE TIMESTAMPTZ USING "start_time"::TIMESTAMPTZ;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "session" ALTER COLUMN "start_time" TYPE TIMESTAMPTZ USING "start_time"::TIMESTAMPTZ;
        ALTER TABLE "session" ALTER COLUMN "start_time" TYPE TIMESTAMPTZ USING "start_time"::TIMESTAMPTZ;"""
