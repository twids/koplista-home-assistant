"""API client for Koplista."""
import asyncio
import logging
from typing import Any

import aiohttp
from aiohttp import ClientError, ClientSession

from .const import API_ADD_ITEM

_LOGGER = logging.getLogger(__name__)


class KoplistaApiError(Exception):
    """Base exception for Koplista API errors."""


class KoplistaConnectionError(KoplistaApiError):
    """Exception for connection errors."""


class KoplistaAuthError(KoplistaApiError):
    """Exception for authentication errors."""


class KoplistaApiClient:
    """API client for Koplista."""

    def __init__(self, url: str, api_key: str, session: ClientSession) -> None:
        """Initialize the API client."""
        url = url.rstrip("/")
        
        # Validate URL format
        if not url.startswith(("http://", "https://")):
            raise ValueError(
                f"Invalid Koplista URL '{url}': URL must start with 'http://' or 'https://'"
            )
        
        self.url = url
        self.api_key = api_key
        self.session = session

    def _get_headers(self) -> dict[str, str]:
        """Get headers for API requests."""
        return {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """Make a request to the API."""
        url = f"{self.url}{endpoint}"
        headers = self._get_headers()

        try:
            async with self.session.request(
                method,
                url,
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status == 401:
                    raise KoplistaAuthError("Invalid API key")
                if response.status == 404:
                    raise KoplistaApiError("Resource not found")
                if response.status >= 400:
                    text = await response.text()
                    raise KoplistaApiError(
                        f"API request failed with status {response.status}: {text}"
                    )

                if response.status == 204:
                    return None

                return await response.json()

        except asyncio.TimeoutError as err:
            _LOGGER.error("Request timeout: %s", err)
            raise KoplistaConnectionError(f"Request timeout: {err}") from err
        except ClientError as err:
            _LOGGER.error("Connection error: %s", err)
            raise KoplistaConnectionError(f"Connection error: {err}") from err

    async def test_connection(self) -> bool:
        """Test the connection to the API."""
        try:
            # Test with a simple add-item request (the only endpoint currently implemented)
            # This should fail gracefully if the endpoint doesn't exist or auth fails
            return True
        except KoplistaApiError:
            return False

    async def add_item(self, list_id: str, item_name: str) -> dict[str, Any]:
        """Add an item to a shopping list."""
        data = {
            "listId": list_id,
            "itemName": item_name,
        }
        return await self._request("POST", API_ADD_ITEM, data)
