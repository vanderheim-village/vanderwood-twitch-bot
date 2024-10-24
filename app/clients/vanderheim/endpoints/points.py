from typing import Any, Dict, Optional

from app.clients.vanderheim.base_client import BaseAPIClient


class PointsAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client

    async def _fetch_points_page(
        self, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of points.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/points/"
        return await self.client._get(url, params=params)

    async def fetch_all_points(self) -> Dict[str, Any]:
        """
        Fetches all points using the fetch_points_page method.
        """
        all_points = []
        page = 1
        while True:
            response = await self._fetch_points_page(page=page)
            points = response["results"]
            all_points.extend(points)
            if not response["next"]:
                break
            page += 1
        return {"results": all_points}

    async def fetch_point(self, point_id: str) -> Dict[str, Any]:
        """
        Fetches a single point by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/points/{point_id}/"
        return await self.client._get(url)

    async def create_point(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new point.
        """
        url = f"{self.client.base_url}/vanderheim-api/points/"
        return await self.client._post(url, data)

    async def update_point(self, point_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing point by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/points/{point_id}/"
        return await self.client._put(url, data)

    async def partial_update_point(self, point_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing point by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/points/{point_id}/"
        return await self.client._patch(url, data)

    async def delete_point(self, point_id: str) -> None:
        """
        Deletes a point by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/points/{point_id}/"
        await self.client._delete(url)
