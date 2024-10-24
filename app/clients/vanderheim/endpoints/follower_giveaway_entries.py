from typing import Any, Dict, Optional

from app.clients.vanderheim.base_client import BaseAPIClient


class FollowerGiveawayEntriesAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client

    async def _fetch_follower_giveaway_entries_page(
        self, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of follower giveaway entries.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/follower-giveaway-entries/"
        return await self.client._get(url, params=params)

    async def fetch_all_follower_giveaway_entries(self) -> Dict[str, Any]:
        """
        Fetches all follower giveaway entries using the fetch_follower_giveaway_entries_page method.
        """
        all_follower_giveaway_entries = []
        page = 1
        while True:
            response = await self._fetch_follower_giveaway_entries_page(page=page)
            follower_giveaway_entries = response["results"]
            all_follower_giveaway_entries.extend(follower_giveaway_entries)
            if not response["next"]:
                break
            page += 1
        return {"results": all_follower_giveaway_entries}

    async def fetch_follower_giveaway_entry(
        self, follower_giveaway_entry_id: str
    ) -> Dict[str, Any]:
        """
        Fetches a single follower giveaway entry by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/follower-giveaway-entries/{follower_giveaway_entry_id}/"
        return await self.client._get(url)

    async def create_follower_giveaway_entry(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new follower giveaway entry.
        """
        url = f"{self.client.base_url}/vanderheim-api/follower-giveaway-entries/"
        return await self.client._post(url, data)

    async def update_follower_giveaway_entry(
        self, follower_giveaway_entry_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing follower giveaway entry by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/follower-giveaway-entries/{follower_giveaway_entry_id}/"
        return await self.client._put(url, data)

    async def partial_update_follower_giveaway_entry(
        self, follower_giveaway_entry_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing follower giveaway entry by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/follower-giveaway-entries/{follower_giveaway_entry_id}/"
        return await self.client._patch(url, data)

    async def delete_follower_giveaway_entry(self, follower_giveaway_entry_id: str) -> None:
        """
        Deletes a follower giveaway entry by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/follower-giveaway-entries/{follower_giveaway_entry_id}/"
        await self.client._delete(url)
