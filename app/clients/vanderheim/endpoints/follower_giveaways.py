from typing import Any, Dict, Optional

from app.clients.vanderheim.base_client import BaseAPIClient


class FollowerGiveawaysAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client

    async def _fetch_follower_giveaways_page(
        self, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of follower giveaways.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/follower-giveaways/"
        return await self.client._get(url, params=params)

    async def fetch_all_follower_giveaways(self) -> Dict[str, Any]:
        """
        Fetches all follower giveaways using the fetch_follower_giveaways_page method.
        """
        all_follower_giveaways = []
        page = 1
        while True:
            response = await self._fetch_follower_giveaways_page(page=page)
            follower_giveaways = response["results"]
            all_follower_giveaways.extend(follower_giveaways)
            if not response["next"]:
                break
            page += 1
        return {"results": all_follower_giveaways}

    async def fetch_follower_giveaway(self, follower_giveaway_id: str) -> Dict[str, Any]:
        """
        Fetches a single follower giveaway by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/follower-giveaways/{follower_giveaway_id}/"
        return await self.client._get(url)

    async def create_follower_giveaway(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new follower giveaway.
        """
        url = f"{self.client.base_url}/vanderheim-api/follower-giveaways/"
        return await self.client._post(url, data)

    async def update_follower_giveaway(
        self, follower_giveaway_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing follower giveaway by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/follower-giveaways/{follower_giveaway_id}/"
        return await self.client._put(url, data)

    async def partial_update_follower_giveaway(
        self, follower_giveaway_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing follower giveaway by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/follower-giveaways/{follower_giveaway_id}/"
        return await self.client._patch(url, data)

    async def delete_follower_giveaway(self, follower_giveaway_id: str) -> None:
        """
        Deletes a single follower giveaway by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/follower-giveaways/{follower_giveaway_id}/"
        await self.client._delete(url)
