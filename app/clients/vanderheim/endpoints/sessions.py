from typing import Any, Dict, Optional

from app.clients.vanderheim.base_client import BaseAPIClient


class SessionsAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client

    async def _fetch_sessions_page(
        self, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of sessions.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/sessions/"
        return await self.client._get(url, params=params)

    async def fetch_all_sessions(self) -> Dict[str, Any]:
        """
        Fetches all sessions using the fetch_sessions_page method.
        """
        all_sessions = []
        page = 1
        while True:
            response = await self._fetch_sessions_page(page=page)
            sessions = response["results"]
            all_sessions.extend(sessions)
            if not response["next"]:
                break
            page += 1
        return {"results": all_sessions}

    async def fetch_session(self, session_id: str) -> Dict[str, Any]:
        """
        Fetches a single session by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/sessions/{session_id}/"
        return await self.client._get(url)

    async def create_session(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new session.
        """
        url = f"{self.client.base_url}/vanderheim-api/sessions/"
        return await self.client._post(url, data)

    async def update_session(self, session_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing session by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/sessions/{session_id}/"
        return await self.client._put(url, data)

    async def partial_update_session(self, session_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing session by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/sessions/{session_id}/"
        return await self.client._patch(url, data)

    async def delete_session(self, session_id: str) -> None:
        """
        Deletes a session by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/sessions/{session_id}/"
        await self.client._delete(url)
