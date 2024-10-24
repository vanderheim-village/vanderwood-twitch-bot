from typing import Any, Dict, Optional

from app.clients.vanderheim.base_client import BaseAPIClient


class SentryCheckinsAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client

    async def _fetch_sentry_checkins_page(
        self, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of sentry checkins.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/sentry-checkins/"
        return await self.client._get(url, params=params)

    async def fetch_all_sentry_checkins(self) -> Dict[str, Any]:
        """
        Fetches all sentry checkins using the fetch_sentry_checkins_page method.
        """
        all_sentry_checkins = []
        page = 1
        while True:
            response = await self._fetch_sentry_checkins_page(page=page)
            sentry_checkins = response["results"]
            all_sentry_checkins.extend(sentry_checkins)
            if not response["next"]:
                break
            page += 1
        return {"results": all_sentry_checkins}

    async def fetch_sentry_checkin(self, sentry_checkin_id: str) -> Dict[str, Any]:
        """
        Fetches a single sentry checkin by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/sentry-checkins/{sentry_checkin_id}/"
        return await self.client._get(url)

    async def create_sentry_checkin(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new sentry checkin.
        """
        url = f"{self.client.base_url}/vanderheim-api/sentry-checkins/"
        return await self.client._post(url, data)

    async def update_sentry_checkin(
        self, sentry_checkin_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing sentry checkin by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/sentry-checkins/{sentry_checkin_id}/"
        return await self.client._put(url, data)

    async def partial_update_sentry_checkin(
        self, sentry_checkin_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing sentry checkin by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/sentry-checkins/{sentry_checkin_id}/"
        return await self.client._patch(url, data)

    async def delete_sentry_checkin(self, sentry_checkin_id: str) -> None:
        """
        Deletes a sentry checkin by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/sentry-checkins/{sentry_checkin_id}/"
        await self.client._delete(url)
