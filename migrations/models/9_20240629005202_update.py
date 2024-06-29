from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "checkin" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "checkin" ALTER COLUMN "session_id" TYPE INT USING "session_id"::INT;
        ALTER TABLE "checkin" ALTER COLUMN "player_id" TYPE INT USING "player_id"::INT;
        ALTER TABLE "clan" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "followergiveaway" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "followergiveaway" ALTER COLUMN "winner_id" TYPE INT USING "winner_id"::INT;
        ALTER TABLE "followergiveawayentry" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "followergiveawayentry" ALTER COLUMN "player_id" TYPE INT USING "player_id"::INT;
        ALTER TABLE "followergiveawayentry" ALTER COLUMN "giveaway_id" TYPE INT USING "giveaway_id"::INT;
        ALTER TABLE "followergiveawayprize" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "giftedsubsleaderboard" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "giftedsubsleaderboard" ALTER COLUMN "player_id" TYPE INT USING "player_id"::INT;
        ALTER TABLE "player" ALTER COLUMN "clan_id" TYPE INT USING "clan_id"::INT;
        ALTER TABLE "player" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "points" ALTER COLUMN "season_id" TYPE INT USING "season_id"::INT;
        ALTER TABLE "points" ALTER COLUMN "clan_id" TYPE INT USING "clan_id"::INT;
        ALTER TABLE "points" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "points" ALTER COLUMN "player_id" TYPE INT USING "player_id"::INT;
        ALTER TABLE "raidcheckin" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "raidcheckin" ALTER COLUMN "session_id" TYPE INT USING "session_id"::INT;
        ALTER TABLE "raidcheckin" ALTER COLUMN "player_id" TYPE INT USING "player_id"::INT;
        ALTER TABLE "raidsession" ALTER COLUMN "season_id" TYPE INT USING "season_id"::INT;
        ALTER TABLE "raidsession" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "rewardlevel" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "season" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "session" ALTER COLUMN "season_id" TYPE INT USING "season_id"::INT;
        ALTER TABLE "session" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "subscriptions" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "subscriptions" ALTER COLUMN "player_id" TYPE INT USING "player_id"::INT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "clan" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "player" ALTER COLUMN "clan_id" TYPE INT USING "clan_id"::INT;
        ALTER TABLE "player" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "points" ALTER COLUMN "season_id" TYPE INT USING "season_id"::INT;
        ALTER TABLE "points" ALTER COLUMN "clan_id" TYPE INT USING "clan_id"::INT;
        ALTER TABLE "points" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "points" ALTER COLUMN "player_id" TYPE INT USING "player_id"::INT;
        ALTER TABLE "season" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "checkin" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "checkin" ALTER COLUMN "session_id" TYPE INT USING "session_id"::INT;
        ALTER TABLE "checkin" ALTER COLUMN "player_id" TYPE INT USING "player_id"::INT;
        ALTER TABLE "session" ALTER COLUMN "season_id" TYPE INT USING "season_id"::INT;
        ALTER TABLE "session" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "raidcheckin" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "raidcheckin" ALTER COLUMN "session_id" TYPE INT USING "session_id"::INT;
        ALTER TABLE "raidcheckin" ALTER COLUMN "player_id" TYPE INT USING "player_id"::INT;
        ALTER TABLE "raidsession" ALTER COLUMN "season_id" TYPE INT USING "season_id"::INT;
        ALTER TABLE "raidsession" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "rewardlevel" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "subscriptions" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "subscriptions" ALTER COLUMN "player_id" TYPE INT USING "player_id"::INT;
        ALTER TABLE "followergiveaway" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "followergiveaway" ALTER COLUMN "winner_id" TYPE INT USING "winner_id"::INT;
        ALTER TABLE "followergiveawayentry" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "followergiveawayentry" ALTER COLUMN "player_id" TYPE INT USING "player_id"::INT;
        ALTER TABLE "followergiveawayentry" ALTER COLUMN "giveaway_id" TYPE INT USING "giveaway_id"::INT;
        ALTER TABLE "followergiveawayprize" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "giftedsubsleaderboard" ALTER COLUMN "channel_id" TYPE INT USING "channel_id"::INT;
        ALTER TABLE "giftedsubsleaderboard" ALTER COLUMN "player_id" TYPE INT USING "player_id"::INT;"""
