from typing import Any, Dict, Optional

from app.clients.vanderheim.base_client import BaseAPIClient


class RaidCheckinsAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client

    def _fetch_raid_checkins_page(
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
        return self.client._get(url, params=params)

    def fetch_all_raid_checkins(self) -> Dict[str, Any]:
        """
        Fetches all raid checkins using the fetch_raid_checkins_page method.
        """
        all_raid_checkins = []
        page = 1
        while True:
            response = self._fetch_raid_checkins_page(page=page)
            raid_checkins = response["results"]
            all_raid_checkins.extend(raid_checkins)
            if not response["next"]:
                break
            page += 1
        return {"results": all_raid_checkins}

    def fetch_raid_checkin(self, raid_checkin_id: str) -> Dict[str, Any]:
        """
        Fetches a single raid checkin by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/raid-checkins/{raid_checkin_id}/"
        return self.client._get(url)

    def create_raid_checkin(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new raid checkin.
        """
        url = f"{self.client.base_url}/vanderheim-api/raid-checkins/"
        return self.client._post(url, data)

    def update_raid_checkin(self, raid_checkin_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing raid checkin by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/raid-checkins/{raid_checkin_id}/"
        return self.client._put(url, data)

    def partial_update_raid_checkin(
        self, raid_checkin_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing raid checkin by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/raid-checkins/{raid_checkin_id}/"
        return self.client._patch(url, data)

    def delete_raid_checkin(self, raid_checkin_id: str) -> None:
        """
        Deletes a raid checkin by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/raid-checkins/{raid_checkin_id}/"
        self.client._delete(url)
