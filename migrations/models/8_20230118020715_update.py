from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "channel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE
);;
        ALTER TABLE "checkin" ADD "channel_id" INT NOT NULL;
        ALTER TABLE "clan" ADD "channel_id" INT NOT NULL;
        ALTER TABLE "player" ADD "channel_id" INT NOT NULL;
        ALTER TABLE "points" ADD "channel_id" INT NOT NULL;
        ALTER TABLE "season" ADD "channel_id" INT NOT NULL;
        ALTER TABLE "session" ADD "channel_id" INT NOT NULL;
        ALTER TABLE "subscriptions" ADD "channel_id" INT NOT NULL;
        ALTER TABLE "checkin" ADD CONSTRAINT "fk_checkin_channel_acdf8121" FOREIGN KEY ("channel_id") REFERENCES "channel" ("id") ON DELETE CASCADE;
        ALTER TABLE "clan" ADD CONSTRAINT "fk_clan_channel_90e70f8a" FOREIGN KEY ("channel_id") REFERENCES "channel" ("id") ON DELETE CASCADE;
        ALTER TABLE "player" ADD CONSTRAINT "fk_player_channel_5651eb6a" FOREIGN KEY ("channel_id") REFERENCES "channel" ("id") ON DELETE CASCADE;
        ALTER TABLE "points" ADD CONSTRAINT "fk_points_channel_b743a54b" FOREIGN KEY ("channel_id") REFERENCES "channel" ("id") ON DELETE CASCADE;
        ALTER TABLE "season" ADD CONSTRAINT "fk_season_channel_74214f87" FOREIGN KEY ("channel_id") REFERENCES "channel" ("id") ON DELETE CASCADE;
        ALTER TABLE "session" ADD CONSTRAINT "fk_session_channel_d333348d" FOREIGN KEY ("channel_id") REFERENCES "channel" ("id") ON DELETE CASCADE;
        ALTER TABLE "subscriptions" ADD CONSTRAINT "fk_subscrip_channel_cb0e557f" FOREIGN KEY ("channel_id") REFERENCES "channel" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "subscriptions" DROP CONSTRAINT "fk_subscrip_channel_cb0e557f";
        ALTER TABLE "session" DROP CONSTRAINT "fk_session_channel_d333348d";
        ALTER TABLE "checkin" DROP CONSTRAINT "fk_checkin_channel_acdf8121";
        ALTER TABLE "season" DROP CONSTRAINT "fk_season_channel_74214f87";
        ALTER TABLE "points" DROP CONSTRAINT "fk_points_channel_b743a54b";
        ALTER TABLE "player" DROP CONSTRAINT "fk_player_channel_5651eb6a";
        ALTER TABLE "clan" DROP CONSTRAINT "fk_clan_channel_90e70f8a";
        ALTER TABLE "clan" DROP COLUMN "channel_id";
        ALTER TABLE "player" DROP COLUMN "channel_id";
        ALTER TABLE "points" DROP COLUMN "channel_id";
        ALTER TABLE "season" DROP COLUMN "channel_id";
        ALTER TABLE "checkin" DROP COLUMN "channel_id";
        ALTER TABLE "session" DROP COLUMN "channel_id";
        ALTER TABLE "subscriptions" DROP COLUMN "channel_id";
        DROP TABLE IF EXISTS "channel";"""
