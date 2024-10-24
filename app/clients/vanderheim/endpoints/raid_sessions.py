from typing import Any, Dict, Optional

from app.clients.vanderheim.base_client import BaseAPIClient


class RaidSessionsAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client

    def _fetch_raid_sessions_page(
        self, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of raid sessions.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/raid-sessions/"
        return self.client._get(url, params=params)

    def fetch_all_raid_sessions(self) -> Dict[str, Any]:
        """
        Fetches all raid sessions using the fetch_raid_sessions_page method.
        """
        all_raid_sessions = []
        page = 1
        while True:
            response = self._fetch_raid_sessions_page(page=page)
            raid_sessions = response["results"]
            all_raid_sessions.extend(raid_sessions)
            if not response["next"]:
                break
            page += 1
        return {"results": all_raid_sessions}

    def fetch_raid_session(self, raid_session_id: str) -> Dict[str, Any]:
        """
        Fetches a single raid session by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/raid-sessions/{raid_session_id}/"
        return self.client._get(url)

    def create_raid_session(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new raid session.
        """
        url = f"{self.client.base_url}/vanderheim-api/raid-sessions/"
        return self.client._post(url, data)

    def update_raid_session(self, raid_session_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing raid session by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/raid-sessions/{raid_session_id}/"
        return self.client._put(url, data)

    def partial_update_raid_session(
        self, raid_session_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing raid session by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/raid-sessions/{raid_session_id}/"
        return self.client._patch(url, data)

    def delete_raid_session(self, raid_session_id: str) -> None:
        """
        Deletes an existing raid session by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/raid-sessions/{raid_session_id}/"
        self.client._delete(url)
