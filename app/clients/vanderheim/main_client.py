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
from app.clients.vanderheim.endpoints.raid_sessions import RaidSessionsAPI


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
        self.raid_sessions = RaidSessionsAPI(self.base_client)
