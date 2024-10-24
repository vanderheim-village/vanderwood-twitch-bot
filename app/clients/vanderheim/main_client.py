from app.clients.vanderheim.base_client import BaseAPIClient
from app.clients.vanderheim.endpoints.checkins import CheckinsAPI
from app.clients.vanderheim.endpoints.clan_spoils_claims import ClanSpoilsClaimsAPI
from app.clients.vanderheim.endpoints.clan_spoils_sessions import ClanSpoilsSessionsAPI
from app.clients.vanderheim.endpoints.clans import ClansAPI
from app.clients.vanderheim.endpoints.follower_giveaway_entries import FollowerGiveawayEntriesAPI
from app.clients.vanderheim.endpoints.follower_giveaway_prizes import FollowerGiveawayPrizesAPI
from app.clients.vanderheim.endpoints.follower_giveaways import FollowerGiveawaysAPI
from app.clients.vanderheim.endpoints.gifted_subscriptions import GiftedSubscriptionsAPI
from app.clients.vanderheim.endpoints.player_watch_times import PlayerWatchTimesAPI
from app.clients.vanderheim.endpoints.players import PlayersAPI
from app.clients.vanderheim.endpoints.points import PointsAPI
from app.clients.vanderheim.endpoints.raid_checkins import RaidCheckinsAPI
from app.clients.vanderheim.endpoints.raid_sessions import RaidSessionsAPI
from app.clients.vanderheim.endpoints.seasons import SeasonsAPI
from app.clients.vanderheim.endpoints.sentry_checkins import SentryCheckinsAPI
from app.clients.vanderheim.endpoints.sentry_sessions import SentrySessionsAPI
from app.clients.vanderheim.endpoints.sessions import SessionsAPI
from app.clients.vanderheim.endpoints.spoils_claims import SpoilsClaimsAPI
from app.clients.vanderheim.endpoints.spoils_sessions import SpoilsSessionsAPI
from app.clients.vanderheim.endpoints.subscriptions import SubscriptionsAPI


class VanderheimAPIClient:
    def __init__(self, base_url: str, api_token: str):
        self.base_client = BaseAPIClient(base_url, api_token)
        self.checkins = CheckinsAPI(self.base_client)
        self.clan_spoils_claims = ClanSpoilsClaimsAPI(self.base_client)
        self.clan_spoils_sessions = ClanSpoilsSessionsAPI(self.base_client)
        self.clans = ClansAPI(self.base_client)
        self.follower_giveaway_entries = FollowerGiveawayEntriesAPI(self.base_client)
        self.follower_giveaway_prizes = FollowerGiveawayPrizesAPI(self.base_client)
        self.follower_giveaways = FollowerGiveawaysAPI(self.base_client)
        self.gifted_subscriptions = GiftedSubscriptionsAPI(self.base_client)
        self.player_watch_times = PlayerWatchTimesAPI(self.base_client)
        self.players = PlayersAPI(self.base_client)
        self.points = PointsAPI(self.base_client)
        self.raid_checkins = RaidCheckinsAPI(self.base_client)
        self.raid_sessions = RaidSessionsAPI(self.base_client)
        self.seasons = SeasonsAPI(self.base_client)
        self.sentry_checkins = SentryCheckinsAPI(self.base_client)
        self.sentry_sessions = SentrySessionsAPI(self.base_client)
        self.sessions = SessionsAPI(self.base_client)
        self.spoils_claims = SpoilsClaimsAPI(self.base_client)
        self.spoils_sessions = SpoilsSessionsAPI(self.base_client)
        self.subscriptions = SubscriptionsAPI(self.base_client)
