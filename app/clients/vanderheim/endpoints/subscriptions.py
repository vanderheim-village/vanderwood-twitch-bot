from typing import Any, Dict, Optional

from app.clients.vanderheim.base_client import BaseAPIClient


class SubscriptionsAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client

    async def _fetch_subscriptions_page(
        self, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of subscriptions.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/subscriptions/"
        return await self.client._get(url, params=params)

    async def fetch_all_subscriptions(self) -> Dict[str, Any]:
        """
        Fetches all subscriptions using the fetch_subscriptions_page method.
        """
        all_subscriptions = []
        page = 1
        while True:
            response = await self._fetch_subscriptions_page(page=page)
            subscriptions = response["results"]
            all_subscriptions.extend(subscriptions)
            if not response["next"]:
                break
            page += 1
        return {"results": all_subscriptions}

    async def fetch_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """
        Fetches a single subscription by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/subscriptions/{subscription_id}/"
        return await self.client._get(url)

    async def create_subscription(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new subscription.
        """
        url = f"{self.client.base_url}/vanderheim-api/subscriptions/"
        return await self.client._post(url, data)

    async def update_subscription(
        self, subscription_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing subscription by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/subscriptions/{subscription_id}/"
        return await self.client._put(url, data)

    async def partial_update_subscription(
        self, subscription_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing subscription by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/subscriptions/{subscription_id}/"
        return await self.client._patch(url, data)

    async def delete_subscription(self, subscription_id: str) -> None:
        """
        Deletes a subscription by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/subscriptions/{subscription_id}/"
        await self.client._delete(url)
