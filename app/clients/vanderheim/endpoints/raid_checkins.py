from typing import Any, Dict, Optional

from app.clients.vanderheim.base_client import BaseAPIClient


class RaidCheckinsAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client

    async def _fetch_raid_checkins_page(
        self, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of raid checkins.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/raid-checkins/"
        return await self.client._get(url, params=params)

    async def fetch_all_raid_checkins(self) -> Dict[str, Any]:
        """
        Fetches all raid checkins using the fetch_raid_checkins_page method.
        """
        all_raid_checkins = []
        page = 1
        while True:
            response = await self._fetch_raid_checkins_page(page=page)
            raid_checkins = response["results"]
            all_raid_checkins.extend(raid_checkins)
            if not response["next"]:
                break
            page += 1
        return {"results": all_raid_checkins}

    async def fetch_raid_checkin(self, raid_checkin_id: str) -> Dict[str, Any]:
        """
        Fetches a single raid checkin by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/raid-checkins/{raid_checkin_id}/"
        return await self.client._get(url)

    async def create_raid_checkin(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new raid checkin.
        """
        url = f"{self.client.base_url}/vanderheim-api/raid-checkins/"
        return await self.client._post(url, data)

    async def update_raid_checkin(
        self, raid_checkin_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing raid checkin by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/raid-checkins/{raid_checkin_id}/"
        return await self.client._put(url, data)

    async def partial_update_raid_checkin(
        self, raid_checkin_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing raid checkin by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/raid-checkins/{raid_checkin_id}/"
        return await self.client._patch(url, data)

    async def delete_raid_checkin(self, raid_checkin_id: str) -> None:
        """
        Deletes a raid checkin by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/raid-checkins/{raid_checkin_id}/"
        await self.client._delete(url)
