from app.clients.vanderheim.base_client import BaseAPIClient
from app.clients.vanderheim.endpoints.checkins import CheckinsAPI


class VanderheimAPIClient:
    def __init__(self, base_url: str, api_token: str):
        self.base_client = BaseAPIClient(base_url, api_token)
        self.checkins = CheckinsAPI(self.base_client)
