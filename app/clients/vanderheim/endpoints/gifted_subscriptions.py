from typing import Optional, Dict, Any

from app.clients.vanderheim.base_client import BaseAPIClient


class GiftedSubscriptionsAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client
    
    def _fetch_gifted_subscriptions_page(self, page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of gifted subscriptions.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/gifted-subscriptions/"
        return self.client._get(url, params=params)
    
    def fetch_all_gifted_subscriptions(self) -> Dict[str, Any]:
        """
        Fetches all gifted subscriptions using the fetch_gifted_subscriptions_page method.
        """
        all_gifted_subscriptions = []
        page = 1
        while True:
            response = self._fetch_gifted_subscriptions_page(page=page)
            gifted_subscriptions = response["results"]
            all_gifted_subscriptions.extend(gifted_subscriptions)
            if not response["next"]:
                break
            page += 1
        return {"results": all_gifted_subscriptions}
    
    def fetch_gifted_subscription(self, gifted_subscription_id: int) -> Dict[str, Any]:
        """
        Fetches a single gifted subscription by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/gifted-subscriptions/{gifted_subscription_id}/"
        return self.client._get(url)
    
    def create_gifted_subscription(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new gifted subscription.
        """
        url = f"{self.client.base_url}/vanderheim-api/gifted-subscriptions/"
        return self.client._post(url, data)
    
    def update_gifted_subscription(self, gifted_subscription_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing gifted subscription by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/gifted-subscriptions/{gifted_subscription_id}/"
        return self.client._put(url, data)
    
    def partial_update_gifted_subscription(self, gifted_subscription_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing gifted subscription by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/gifted-subscriptions/{gifted_subscription_id}/"
        return self.client._patch(url, data)
    
    def delete_gifted_subscription(self, gifted_subscription_id: int) -> None:
        """
        Deletes a single gifted subscription by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/gifted-subscriptions/{gifted_subscription_id}/"
        return self.client._delete(url)
