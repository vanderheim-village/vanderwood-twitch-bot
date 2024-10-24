from typing import Any, Dict

import aiohttp
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class BaseAPIClient:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

    async def _get(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=self.headers) as response:
                    return await response.json()
        except aiohttp.ClientResponseError as e:
            logger.error(f"GET request failed with status {e.status} and message {e.message}")
            raise


    async def _post(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, headers=self.headers) as response:
                    return await response.json()
        except aiohttp.ClientResponseError as e:
            logger.error(f"POST request failed with status {e.status} and message {e.message}")
            raise

    async def _put(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(url, json=data, headers=self.headers) as response:
                    return await response.json()
        except aiohttp.ClientResponseError as e:
            logger.error(f"PUT request failed with status {e.status} and message {e.message}")
            raise
        
    async def _patch(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(url, json=data, headers=self.headers) as response:
                    return await response.json()
        except aiohttp.ClientResponseError as e:
            logger.error(f"PATCH request failed with status {e.status} and message {e.message}")
            raise
    
    async def _delete(self, url: str) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.delete(url, headers=self.headers) as response:
                    return response.status == 204
        except aiohttp.ClientResponseError as e:
            logger.error(f"DELETE request failed with status {e.status} and message {e.message}")
            raise
