from typing import Any, Dict, Optional

from app.clients.vanderheim.base_client import BaseAPIClient


class ClanSpoilsSessionsAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client

    async def _fetch_clan_spoils_sessions_page(
        self, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of clan spoils sessions.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/clan-spoils-sessions/"
        return await self.client._get(url, params=params)

    async def fetch_all_clan_spoils_sessions(self) -> Dict[str, Any]:
        """
        Fetches all clan spoils sessions using the fetch_clan_spoils_sessions_page method.
        """
        all_clan_spoils_sessions = []
        page = 1
        while True:
            response = await self._fetch_clan_spoils_sessions_page(page=page)
            clan_spoils_sessions = response["results"]
            all_clan_spoils_sessions.extend(clan_spoils_sessions)
            if not response["next"]:
                break
            page += 1
        return {"results": all_clan_spoils_sessions}

    async def fetch_clan_spoils_session(self, clan_spoils_session_id: str) -> Dict[str, Any]:
        """
        Fetches a single clan spoils session by ID.
        """
        url = (
            f"{self.client.base_url}/vanderheim-api/clan-spoils-sessions/{clan_spoils_session_id}/"
        )
        return await self.client._get(url)

    async def create_clan_spoils_session(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new clan spoils session.
        """
        url = f"{self.client.base_url}/vanderheim-api/clan-spoils-sessions/"
        return await self.client._post(url, data)

    async def update_clan_spoils_session(
        self, clan_spoils_session_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing clan spoils session by ID.
        """
        url = (
            f"{self.client.base_url}/vanderheim-api/clan-spoils-sessions/{clan_spoils_session_id}/"
        )
        return await self.client._put(url, data)

    async def partial_update_clan_spoils_session(
        self, clan_spoils_session_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing clan spoils session by ID.
        """
        url = (
            f"{self.client.base_url}/vanderheim-api/clan-spoils-sessions/{clan_spoils_session_id}/"
        )
        return await self.client._patch(url, data)

    async def delete_clan_spoils_session(self, clan_spoils_session_id: str) -> None:
        """
        Deletes a clan spoils session by ID.
        """
        url = (
            f"{self.client.base_url}/vanderheim-api/clan-spoils-sessions/{clan_spoils_session_id}/"
        )
        await self.client._delete(url)
