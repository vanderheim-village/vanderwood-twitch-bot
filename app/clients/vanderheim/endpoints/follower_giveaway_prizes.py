from typing import Any, Dict, Optional

from app.clients.vanderheim.base_client import BaseAPIClient


class FollowerGiveawayPrizesAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client

    def _fetch_follower_giveaway_prizes_page(
        self, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of follower giveaway prizes.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/follower-giveaway-prizes/"
        return self.client._get(url, params=params)

    def fetch_all_follower_giveaway_prizes(self) -> Dict[str, Any]:
        """
        Fetches all follower giveaway prizes using the fetch_follower_giveaway_prizes_page method.
        """
        all_follower_giveaway_prizes = []
        page = 1
        while True:
            response = self._fetch_follower_giveaway_prizes_page(page=page)
            follower_giveaway_prizes = response["results"]
            all_follower_giveaway_prizes.extend(follower_giveaway_prizes)
            if not response["next"]:
                break
            page += 1
        return {"results": all_follower_giveaway_prizes}

    def fetch_follower_giveaway_prize(self, follower_giveaway_prize_id: str) -> Dict[str, Any]:
        """
        Fetches a single follower giveaway prize by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/follower-giveaway-prizes/{follower_giveaway_prize_id}/"
        return self.client._get(url)

    def create_follower_giveaway_prize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new follower giveaway prize.
        """
        url = f"{self.client.base_url}/vanderheim-api/follower-giveaway-prizes/"
        return self.client._post(url, data)

    def update_follower_giveaway_prize(
        self, follower_giveaway_prize_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing follower giveaway prize by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/follower-giveaway-prizes/{follower_giveaway_prize_id}/"
        return self.client._put(url, data)

    def partial_update_follower_giveaway_prize(
        self, follower_giveaway_prize_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing follower giveaway prize by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/follower-giveaway-prizes/{follower_giveaway_prize_id}/"
        return self.client._patch(url, data)

    def delete_follower_giveaway_prize(self, follower_giveaway_prize_id: str) -> None:
        """
        Deletes an existing follower giveaway prize by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/follower-giveaway-prizes/{follower_giveaway_prize_id}/"
        self.client._delete(url)
