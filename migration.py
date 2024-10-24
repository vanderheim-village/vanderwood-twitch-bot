import asyncio
from tortoise import Tortoise
from dotenv import load_dotenv
import os
import logging

from app import settings
from app.clients.vanderheim import VanderheimAPIClient

from app.models import (
    Clan,
    Checkin,
    ClanSpoilsClaim,
    ClanSpoilsSession,
    RaidCheckin,
    RaidSession,
    FollowerGiveaway,
    FollowerGiveawayEntry,
    FollowerGiveawayPrize,
    GiftedSubsLeaderboard,
    Player,
    PlayerWatchTime,
    Points,
    Season,
    SentryCheckin,
    SentrySession,
    Session,
    SpoilsClaim,
    Subscriptions,
    SpoilsSession,
)

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def load_config():
    load_dotenv(".env/.prod")

async def migrate_clans():
    # Setups the Tortoise ORM with the database connection
    await Tortoise.init(
        config = settings.TORTOISE
    )

    # Generate the schema
    await Tortoise.generate_schemas()

    # Create a new Vanderheim API client
    vanderheim_client = VanderheimAPIClient(
        base_url=os.getenv("VANDERHEIM_API_BASE_URL"),
        api_token=os.getenv("VANDERHEIM_API_KEY")
    )

    follower_giveaway_prizes = await FollowerGiveawayPrize.all()

    for prize in follower_giveaway_prizes:
        vanderheim_prize = await vanderheim_client.follower_giveaway_prizes.create_follower_giveaway_prize({
            "message": prize.message,
            "vp_reward": prize.vp_reward,
        })

        prize.new_guid_id = vanderheim_prize["id"]
        await prize.save()

        logger.info(f"Created prize: {vanderheim_prize}")

    seasons = await Season.all()

    for season in seasons:
        vanderheim_season = await vanderheim_client.seasons.create_season({
            "start_date": season.start_date.isoformat(),
            "name": season.name,
        })

        season.new_guid_id = vanderheim_season["id"]
        await season.save()

        logger.info(f"Created season: {vanderheim_season}")

    clans = await Clan.all()

    for clan in clans:
        vanderheim_clan = await vanderheim_client.clans.create_clan({
            "name": clan.name,
            "tag": clan.tag,
            "twitch_emoji_name": clan.twitch_emoji_name,
        })

        clan.new_guid_id = vanderheim_clan["id"]
        await clan.save()

        logger.info(f"Created clan: {vanderheim_clan}")

    sessions = await Session.all()

    for session in sessions:
        vanderheim_session = await vanderheim_client.sessions.create_session(
            data = {
                "season": str((await session.season).new_guid_id),
                "start_time": session.start_time.isoformat(),
                "end_time": session.end_time.isoformat(),
            }
        )

        session.new_guid_id = vanderheim_session["id"]
        await session.save()

        logger.info(f"Created session: {vanderheim_session}")
    
    raid_sessions = await RaidSession.all()

    for raid_session in raid_sessions:
        vanderheim_raid_session = await vanderheim_client.raid_sessions.create_raid_session(
            data = {
                "season": str((await raid_session.season).new_guid_id),
                "start_time": raid_session.start_time.isoformat(),
                "end_time": raid_session.end_time.isoformat(),
            }
        )

        raid_session.new_guid_id = vanderheim_raid_session["id"]
        await raid_session.save()
    
        logger.info(f"Created raid session: {vanderheim_raid_session}")
    
    sentry_sessions = await SentrySession.all()

    for sentry_session in sentry_sessions:
        vanderheim_sentry_session = await vanderheim_client.sentry_sessions.create_sentry_session(
            data = {
                "season": str((await sentry_session.season).new_guid_id),
                "session": str((await sentry_session.session).new_guid_id),
                "start_time": sentry_session.start_time.isoformat(),
                "end_time": sentry_session.end_time.isoformat(),
            }
        )

        sentry_session.new_guid_id = vanderheim_sentry_session["id"]
        await sentry_session.save()
    
        logger.info(f"Created sentry session: {vanderheim_sentry_session}")
    
    spoils_sessions = await SpoilsSession.all()

    for spoils_session in spoils_sessions:
        vanderheim_spoils_session = await vanderheim_client.spoils_sessions.create_spoils_session(
            data = {
                "season": str((await spoils_session.season).new_guid_id),
                "start_time": spoils_session.start_time.isoformat(),
                "end_time": spoils_session.end_time.isoformat(),
                "points_reward": spoils_session.points_reward,
            }
        )

        spoils_session.new_guid_id = vanderheim_spoils_session["id"]
        await spoils_session.save()
    
        logger.info(f"Created spoils session: {vanderheim_spoils_session}")
    
    clan_spoils_sessions = await ClanSpoilsSession.all()

    for clan_spoils_session in clan_spoils_sessions:
        vanderheim_clan_spoils_session = await vanderheim_client.clan_spoils_sessions.create_clan_spoils_session(
            data = {
                "season": str((await clan_spoils_session.season).new_guid_id),
                "start_time": clan_spoils_session.start_time.isoformat(),
                "end_time": clan_spoils_session.end_time.isoformat(),
                "points_reward": clan_spoils_session.points_reward,
                "clan": str((await clan_spoils_session.clan).new_guid_id),
            }
        )

        clan_spoils_session.new_guid_id = vanderheim_clan_spoils_session["id"]
        await clan_spoils_session.save()
    
        logger.info(f"Created clan spoils session: {vanderheim_clan_spoils_session}")
        
    players = await Player.all()

    for player in players:
        vanderheim_player = await vanderheim_client.players.create_player({
            "name": player.name,
            "nickname": player.nickname,
            "enabled": player.enabled,
            "clan": str((await player.clan).new_guid_id),
        })

        player.new_guid_id = vanderheim_player["id"]
        await player.save()
    
        logger.info(f"Created player: {vanderheim_player}")
    
    checkins = await Checkin.all()
    
    for checkin in checkins:
        vanderheim_checkin = await vanderheim_client.checkins.create_checkin({
            "session": str((await checkin.session).new_guid_id),
            "player": str((await checkin.player).new_guid_id),
        })

        checkin.new_guid_id = vanderheim_checkin["id"]
        await checkin.save()
    
        logger.info(f"Created checkin: {vanderheim_checkin}")
    
    raid_checkins = await RaidCheckin.all()

    for raid_checkin in raid_checkins:
        vanderheim_raid_checkin = await vanderheim_client.raid_checkins.create_raid_checkin({
            "session": str((await raid_checkin.session).new_guid_id),
            "player": str((await raid_checkin.player).new_guid_id),
        })

        raid_checkin.new_guid_id = vanderheim_raid_checkin["id"]
        await raid_checkin.save()
    
        logger.info(f"Created raid checkin: {vanderheim_raid_checkin}")
    
    sentry_checkins = await SentryCheckin.all()

    for sentry_checkin in sentry_checkins:
        vanderheim_sentry_checkin = await vanderheim_client.sentry_checkins.create_sentry_checkin({
            "session": str((await sentry_checkin.session).new_guid_id),
            "player": str((await sentry_checkin.player).new_guid_id),
        })

        sentry_checkin.new_guid_id = vanderheim_sentry_checkin["id"]
        await sentry_checkin.save()
    
        logger.info(f"Created sentry checkin: {vanderheim_sentry_checkin}")
    
    spoils_claims = await SpoilsClaim.all()

    for spoils_claim in spoils_claims:
        vanderheim_spoils_claim = await vanderheim_client.spoils_claims.create_spoils_claim({
            "session": str((await spoils_claim.spoils_session).new_guid_id),
            "player": str((await spoils_claim.player).new_guid_id),
        })

        spoils_claim.new_guid_id = vanderheim_spoils_claim["id"]
        await spoils_claim.save()
    
        logger.info(f"Created spoils claim: {vanderheim_spoils_claim}")
    
    clan_spoils_claims = await ClanSpoilsClaim.all()

    for clan_spoils_claim in clan_spoils_claims:
        vanderheim_clan_spoils_claim = await vanderheim_client.clan_spoils_claims.create_clan_spoils_claim({
            "session": str((await clan_spoils_claim.spoils_session).new_guid_id),
            "player": str((await clan_spoils_claim.player).new_guid_id),
        })

        clan_spoils_claim.new_guid_id = vanderheim_clan_spoils_claim["id"]
        await clan_spoils_claim.save()
    
        logger.info(f"Created clan spoils claim: {vanderheim_clan_spoils_claim}")
    
    gifted_subs_leaderboards = await GiftedSubsLeaderboard.all()

    for gifted_subs_leaderboard in gifted_subs_leaderboards:
        vanderheim_gifted_subs_leaderboard = await vanderheim_client.gifted_subscriptions.create_gifted_subscription({
            "player": str((await gifted_subs_leaderboard.player).new_guid_id),
            "gifted_subs": gifted_subs_leaderboard.gifted_subs
        })

        gifted_subs_leaderboard.new_guid_id = vanderheim_gifted_subs_leaderboard["id"]
        await gifted_subs_leaderboard.save()
    
        logger.info(f"Created gifted subs leaderboard: {vanderheim_gifted_subs_leaderboard}")
    
    player_watch_times = await PlayerWatchTime.all()

    for player_watch_time in player_watch_times:
        vanderheim_player_watch_time = await vanderheim_client.player_watch_times.create_player_watch_time({
            "player": str((await player_watch_time.player).new_guid_id),
            "watch_time": player_watch_time.watch_time,
            "season": str((await player_watch_time.season).new_guid_id),
        })

        player_watch_time.new_guid_id = vanderheim_player_watch_time["id"]
        await player_watch_time.save()
    
        logger.info(f"Created player watch time: {vanderheim_player_watch_time}")
    
    points = await Points.all()

    for point in points:
        vanderheim_point = await vanderheim_client.points.create_point({
            "player": str((await point.player).new_guid_id),
            "points": point.points,
            "season": str((await point.season).new_guid_id),
            "clan": str((await point.clan).new_guid_id),
        })

        point.new_guid_id = vanderheim_point["id"]
        await point.save()
    
        logger.info(f"Created point: {vanderheim_point}")
    
    subscriptions = await Subscriptions.all()

    for subscription in subscriptions:
        vanderheim_subscription = await vanderheim_client.subscriptions.create_subscription({
            "player": str((await subscription.player).new_guid_id),
            "months_subscribed": subscription.months_subscribed,
        })

        subscription.new_guid_id = vanderheim_subscription["id"]
        await subscription.save()
    
        logger.info(f"Created subscription: {vanderheim_subscription}")
    
    follower_giveaways = await FollowerGiveaway.all()

    for follower_giveaway in follower_giveaways:
        vanderheim_follower_giveaway = await vanderheim_client.follower_giveaways.create_follower_giveaway({
            "start_time": follower_giveaway.start_time.isoformat(),
            "end_time": follower_giveaway.end_time.isoformat(),
            "follower": follower_giveaway.follower,
            "winner": str((await follower_giveaway.winner).new_guid_id),
        })

        follower_giveaway.new_guid_id = vanderheim_follower_giveaway["id"]
        await follower_giveaway.save()
    
        logger.info(f"Created follower giveaway: {vanderheim_follower_giveaway}")
    
    follower_giveaway_entries = await FollowerGiveawayEntry.all()

    for follower_giveaway_entry in follower_giveaway_entries:
        vanderheim_follower_giveaway_entry = await vanderheim_client.follower_giveaway_entries.create_follower_giveaway_entry({
            "giveaway": str((await follower_giveaway_entry.giveaway).new_guid_id),
            "player": str((await follower_giveaway_entry.player).new_guid_id),
        })

        follower_giveaway_entry.new_guid_id = vanderheim_follower_giveaway_entry["id"]

if __name__ == "__main__":
    load_config()
    asyncio.run(migrate_clans())