from typing import Any, Dict, Optional

from app.clients.vanderheim.base_client import BaseAPIClient


class SubscriptionsAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client

    def _fetch_subscriptions_page(
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
        return self.client._get(url, params=params)

    def fetch_all_subscriptions(self) -> Dict[str, Any]:
        """
        Fetches all subscriptions using the fetch_subscriptions_page method.
        """
        all_subscriptions = []
        page = 1
        while True:
            response = self._fetch_subscriptions_page(page=page)
            subscriptions = response["results"]
            all_subscriptions.extend(subscriptions)
            if not response["next"]:
                break
            page += 1
        return {"results": all_subscriptions}

    def fetch_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """
        Fetches a single subscription by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/subscriptions/{subscription_id}/"
        return self.client._get(url)

    def create_subscription(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new subscription.
        """
        url = f"{self.client.base_url}/vanderheim-api/subscriptions/"
        return self.client._post(url, data)

    def update_subscription(self, subscription_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing subscription by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/subscriptions/{subscription_id}/"
        return self.client._put(url, data)

    def partial_update_subscription(
        self, subscription_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing subscription by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/subscriptions/{subscription_id}/"
        return self.client._patch(url, data)

    def delete_subscription(self, subscription_id: str) -> None:
        """
        Deletes a subscription by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/subscriptions/{subscription_id}/"
        self.client._delete(url)
