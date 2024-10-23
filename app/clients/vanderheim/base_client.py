import aiohttp
from typing import Dict, Any

class BaseAPIClient:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url
        self.headers = {
            'Authorization': f"Token {api_token}",
            'Content-Type': 'application/json',
        }
    
    async def _get(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url, params=params) as response:
                return await response.json()
    
    async def _post(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def _put(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.put(url, json=data) as response:
                return await response.json()
    
    async def _patch(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.patch(url, json=data) as response:
                return await response.json()
    
    async def _delete(self, url: str) -> Dict[str, Any]:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.delete(url) as response:
                return await response.json()