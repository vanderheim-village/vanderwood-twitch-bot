from typing import Optional, Dict, Any

from app.clients.vanderheim.base_client import BaseAPIClient


class CheckinsAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client
    
    async def _fetch_checkins_page(self, page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of check-ins.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/checkins/"
        return await self.client._get(url, params=params)
    
    async def fetch_all_checkins(self) -> Dict[str, Any]:
        """
        Fetches all check-ins using the fetch_checkins_page method.
        """
        all_checkins = []
        page = 1
        while True:
            response = await self._fetch_checkins_page(page=page)
            checkins = response["results"]
            all_checkins.extend(checkins)
            if not response["next"]:
                break
            page += 1
        return {"results": all_checkins}
    
    async def fetch_checkin(self, checkin_id: int) -> Dict[str, Any]:
        """
        Fetches a single check-in by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/checkins/{checkin_id}/"
        return await self.client._get(url)
    
    async def create_checkin(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new check-in.
        """
        url = f"{self.client.base_url}/vanderheim-api/checkins/"
        return await self.client._post(url, data)
    
    async def update_checkin(self, checkin_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing check-in by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/checkins/{checkin_id}/"
        return await self.client._put(url, data)
    
    async def partial_update_checkin(self, checkin_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing check-in by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/checkins/{checkin_id}/"
        return await self.client._patch(url, data)
    
    async def delete_checkin(self, checkin_id: int) -> Dict[str, Any]:
        """
        Deletes a check-in by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/checkins/{checkin_id}/"
        return await self.client._delete(url)