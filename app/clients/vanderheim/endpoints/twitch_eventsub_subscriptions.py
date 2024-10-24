from typing import Any, Dict, Optional

from app.clients.vanderheim.base_client import BaseAPIClient


class TwitchEventSubSubscriptionsAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client

    async def _fetch_twitch_eventsub_subscriptions_page(
        self, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of Twitch EventSub subscriptions.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/twitch-eventsub-subscriptions/"
        return await self.client._get(url, params=params)

    async def fetch_all_twitch_eventsub_subscriptions(self) -> Dict[str, Any]:
        """
        Fetches all Twitch EventSub subscriptions using the fetch_twitch_eventsub_subscriptions_page method.
        """
        all_twitch_eventsub_subscriptions = []
        page = 1
        while True:
            response = await self._fetch_twitch_eventsub_subscriptions_page(page=page)
            twitch_eventsub_subscriptions = response["results"]
            all_twitch_eventsub_subscriptions.extend(twitch_eventsub_subscriptions)
            if not response["next"]:
                break
            page += 1
        return {"results": all_twitch_eventsub_subscriptions}

    async def fetch_twitch_eventsub_subscription(
        self, twitch_eventsub_subscription_id: str
    ) -> Dict[str, Any]:
        """
        Fetches a single Twitch EventSub subscription by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/twitch-eventsub-subscriptions/{twitch_eventsub_subscription_id}/"
        return await self.client._get(url)

    async def create_twitch_eventsub_subscription(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new Twitch EventSub subscription.
        """
        url = f"{self.client.base_url}/vanderheim-api/twitch-eventsub-subscriptions/"
        return await self.client._post(url, data)

    async def update_twitch_eventsub_subscription(
        self, twitch_eventsub_subscription_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing Twitch EventSub subscription by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/twitch-eventsub-subscriptions/{twitch_eventsub_subscription_id}/"
        return await self.client._put(url, data)

    async def partial_update_twitch_eventsub_subscription(
        self, twitch_eventsub_subscription_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing Twitch EventSub subscription by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/twitch-eventsub-subscriptions/{twitch_eventsub_subscription_id}/"
        return await self.client._patch(url, data)

    async def delete_twitch_eventsub_subscription(
        self, twitch_eventsub_subscription_id: str
    ) -> None:
        """
        Deletes a Twitch EventSub subscription by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/twitch-eventsub-subscriptions/{twitch_eventsub_subscription_id}/"
        await self.client._delete(url)
