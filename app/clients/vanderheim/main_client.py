from app.clients.vanderheim.base_client import BaseAPIClient
from app.clients.vanderheim.endpoints.checkins import CheckinsAPI
from app.clients.vanderheim.endpoints.clan_spoils_claims import ClanSpoilsClaimsAPI
from app.clients.vanderheim.endpoints.clan_spoils_sessions import ClanSpoilsSessionsAPI
from app.clients.vanderheim.endpoints.clans import ClansAPI


class VanderheimAPIClient:
    def __init__(self, base_url: str, api_token: str):
        self.base_client = BaseAPIClient(base_url, api_token)
        self.checkins = CheckinsAPI(self.base_client)
        self.clan_spoils_claims = ClanSpoilsClaimsAPI(self.base_client)
        self.clan_spoils_sessions = ClanSpoilsSessionsAPI(self.base_client)
        self.clans = ClansAPI(self.base_client)      