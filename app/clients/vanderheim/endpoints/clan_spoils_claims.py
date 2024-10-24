from typing import Optional, Dict, Any

from app.clients.vanderheim.base_client import BaseAPIClient


class ClanSpoilsClaimsAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client
    
    def _fetch_clan_spoils_claims_page(self, page: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of clan spoils claims.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/clan-spoils-claims/"
        return self.client._get(url, params=params)
    
    def fetch_all_clan_spoils_claims(self) -> Dict[str, Any]:
        """
        Fetches all clan spoils claims using the fetch_clan_spoils_claims_page method.
        """
        all_clan_spoils_claims = []
        page = 1
        while True:
            response = self._fetch_clan_spoils_claims_page(page=page)
            clan_spoils_claims = response["results"]
            all_clan_spoils_claims.extend(clan_spoils_claims)
            if not response["next"]:
                break
            page += 1
        return {"results": all_clan_spoils_claims}
    
    def fetch_clan_spoils_claim(self, clan_spoils_claim_id: str) -> Dict[str, Any]:
        """
        Fetches a single clan spoils claim by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/clan-spoils-claims/{clan_spoils_claim_id}/"
        return self.client._get(url)
    
    def create_clan_spoils_claim(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new clan spoils claim.
        """
        url = f"{self.client.base_url}/vanderheim-api/clan-spoils-claims/"
        return self.client._post(url, data)

    def update_clan_spoils_claim(self, clan_spoils_claim_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing clan spoils claim by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/clan-spoils-claims/{clan_spoils_claim_id}/"
        return self.client._put(url, data)
    
    def partial_update_clan_spoils_claim(self, clan_spoils_claim_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Partially updates an existing clan spoils claim by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/clan-spoils-claims/{clan_spoils_claim_id}/"
        return self.client._patch(url, data)
    
    def delete_clan_spoils_claim(self, clan_spoils_claim_id: str) -> Dict[str, Any]:
        """
        Deletes a clan spoils claim by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/clan-spoils-claims/{clan_spoils_claim_id}/"
        return self.client._delete(url)