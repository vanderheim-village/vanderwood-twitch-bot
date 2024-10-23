from typing import Optional, Dict, Any

from app.clients.vanderheim.base_client import BaseAPIClient


class PlayerWatchTimesAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client
    
    async def _fetch_player_watch_times_page(self, page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of player watch times.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/player-watch-times/"
        return await self.client._get(url, params=params)
    
    async def fetch_all_player_watch_times(self) -> Dict[str, Any]:
        """
        Fetches all player watch times using the fetch_player_watch_times_page method.
        """
        all_player_watch_times = []
        page = 1
        while True:
            response = await self._fetch_player_watch_times_page(page=page)
            player_watch_times = response["results"]
            all_player_watch_times.extend(player_watch_times)
            if not response["next"]:
                break
            page += 1
        return {"results": all_player_watch_times}
    
    async def fetch_player_watch_time(self, player_watch_time_id: int) -> Dict[str, Any]:
        """
        Fetches a single player watch time by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/player-watch-times/{player_watch_time_id}/"
        return await self.client._get(url)
    
    async def create_player_watch_time(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new player watch time.
        """
        url = f"{self.client.base_url}/vanderheim-api/player-watch-times/"
        return await self.client._post(url, data)
    
    async def update_player_watch_time(self, player_watch_time_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing player watch time by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/player-watch-times/{player_watch_time_id}/"
        return await self.client._put(url, data)
    
    async def partial_update_player_watch_time(self, player_watch_time_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing player watch time by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/player-watch-times/{player_watch_time_id}/"
        return await self.client._patch(url, data)
    
    async def delete_player_watch_time(self, player_watch_time_id: int) -> None:
        """
        Deletes an existing player watch time by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/player-watch-times/{player_watch_time_id}/"
        await self.client._delete(url)
