from typing import Any, Dict, Optional

from app.clients.vanderheim.base_client import BaseAPIClient


class SpoilsClaimsAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client

    async def _fetch_spoils_claims_page(
        self, page: Optional[int] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches a single page of a paginated list of spoils claims.
        """
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size

        url = f"{self.client.base_url}/vanderheim-api/spoils-claims/"
        return await self.client._get(url, params=params)

    async def fetch_all_spoils_claims(self) -> Dict[str, Any]:
        """
        Fetches all spoils claims using the fetch_spoils_claims_page method.
        """
        all_spoils_claims = []
        page = 1
        while True:
            response = await self._fetch_spoils_claims_page(page=page)
            spoils_claims = response["results"]
            all_spoils_claims.extend(spoils_claims)
            if not response["next"]:
                break
            page += 1
        return {"results": all_spoils_claims}

    async def fetch_spoils_claim(self, spoils_claim_id: str) -> Dict[str, Any]:
        """
        Fetches a single spoils claim by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/spoils-claims/{spoils_claim_id}/"
        return await self.client._get(url)

    async def create_spoils_claim(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new spoils claim.
        """
        url = f"{self.client.base_url}/vanderheim-api/spoils-claims/"
        return await self.client._post(url, data)

    async def update_spoils_claim(
        self, spoils_claim_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Updates an existing spoils claim by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/spoils-claims/{spoils_claim_id}/"
        return await self.client._put(url, data)

    async def partial_update_spoils_claim(
        self, spoils_claim_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Partially updates an existing spoils claim by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/spoils-claims/{spoils_claim_id}/"
        return await self.client._patch(url, data)

    async def delete_spoils_claim(self, spoils_claim_id: str) -> None:
        """
        Deletes a spoils claim by ID.
        """
        url = f"{self.client.base_url}/vanderheim-api/spoils-claims/{spoils_claim_id}/"
        await self.client._delete(url)
