from app.clients.vanderheim.base_client import BaseAPIClient


class VanderheimAPIClient:
    def __init__(self, base_url: str, api_token: str):
        self.base_client = BaseAPIClient(base_url, api_token)