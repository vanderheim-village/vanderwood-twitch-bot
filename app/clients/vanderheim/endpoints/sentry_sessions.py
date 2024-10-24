from typing import Any, Dict, Optional

from app.clients.vanderheim.base_client import BaseAPIClient


class SentrySessionsAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client

    async def _fetch_sentry_sessions_page(
        self, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of sentry sessions.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/sentry-sessions/"
        return await self.client._get(url, params=params)

    async def fetch_all_sentry_sessions(self) -> Dict[str, Any]:
        """
        Fetches all sentry sessions using the fetch_sentry_sessions_page method.
        """
        all_sentry_sessions = []
        page = 1
        while True:
            response = await self._fetch_sentry_sessions_page(page=page)
            sentry_sessions = response["results"]
            all_sentry_sessions.extend(sentry_sessions)
            if not response["next"]:
                break
            page += 1
        return {"results": all_sentry_sessions}

    async def fetch_sentry_session(self, sentry_session_id: str) -> Dict[str, Any]:
        """
        Fetches a single sentry session by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/sentry-sessions/{sentry_session_id}/"
        return await self.client._get(url)

    async def create_sentry_session(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new sentry session.
        """
        url = f"{self.client.base_url}/vanderheim-api/sentry-sessions/"
        return await self.client._post(url, data)

    async def update_sentry_session(
        self, sentry_session_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing sentry session by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/sentry-sessions/{sentry_session_id}/"
        return await self.client._put(url, data)

    async def partial_update_sentry_session(
        self, sentry_session_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing sentry session by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/sentry-sessions/{sentry_session_id}/"
        return await self.client._patch(url, data)

    async def delete_sentry_session(self, sentry_session_id: str) -> None:
        """
        Deletes a single sentry session by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/sentry-sessions/{sentry_session_id}/"
        await self.client._delete(url)
