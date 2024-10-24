from typing import Optional, Dict, Any

from app.clients.vanderheim.base_client import BaseAPIClient


class ClansAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client
    
    async def _fetch_clans_page(self, page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of clans.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/clans/"
        return await self.client._get(url, params=params)
    
    async def fetch_all_clans(self) -> Dict[str, Any]:
        """
        Fetches all clans using the fetch_clans_page method.
        """
        all_clans = []
        page = 1
        while True:
            response = await self._fetch_clans_page(page=page)
            clans = response["results"]
            all_clans.extend(clans)
            if not response["next"]:
                break
            page += 1
        return {"results": all_clans}
    
    async def fetch_clan(self, clan_id: str) -> Dict[str, Any]:
        """
        Fetches a single clan by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/clans/{clan_id}/"
        return await self.client._get(url)
    
    async def create_clan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new clan.
        """
        url = f"{self.client.base_url}/vanderheim-api/clans/"
        return await self.client._post(url, data)
    
    async def update_clan(self, clan_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing clan by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/clans/{clan_id}/"
        return await self.client._put(url, data)
    
    async def partial_update_clan(self, clan_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing clan by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/clans/{clan_id}/"
        return await self.client._patch(url, data)
    
    async def delete_clan(self, clan_id: str) -> Dict[str, Any]:
        """
        Deletes a clan by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/clans/{clan_id}/"
        return await self.client._delete(url)
    
    async def _fetch_clan_players_page(self, clan_id: str, page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of clan players.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/clans/{clan_id}/players/"
        return await self.client._get(url, params=params)
    
    async def fetch_all_clan_players(self, clan_id: str) -> Dict[str, Any]:
        """
        Fetches all clan players using the fetch_clan_players_page method.
        """
        all_clan_players = []
        page = 1
        while True:
            response = await self._fetch_clan_players_page(clan_id, page=page)
            clan_players = response["results"]
            all_clan_players.extend(clan_players)
            if not response["next"]:
                break
            page += 1
        return {"results": all_clan_players}
    
    async def fetch_clan_player(self, clan_id: str, player_id: str) -> Dict[str, Any]:
        """
        Fetches a single clan player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/clans/{clan_id}/players/{player_id}/"
        return await self.client._get(url)
    
    async def create_clan_player(self, clan_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new clan player.
        """
        url = f"{self.client.base_url}/vanderheim-api/clans/{clan_id}/players/"
        return await self.client._post(url, data)
    
    async def update_clan_player(self, clan_id: str, player_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing clan player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/clans/{clan_id}/players/{player_id}/"
        return await self.client._put(url, data)
    
    async def partial_update_clan_player(self, clan_id: str, player_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing clan player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/clans/{clan_id}/players/{player_id}/"
        return await self.client._patch(url, data)
    
    async def delete_clan_player(self, clan_id: str, player_id: str) -> Dict[str, Any]:
        """
        Deletes a clan player by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/clans/{clan_id}/players/{player_id}/"
        return await self.client._delete(url)
