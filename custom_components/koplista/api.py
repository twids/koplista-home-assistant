"""API client for Koplista.

This client implements communication with the Koplista API.

Current API Limitations:
    The Koplista API currently only implements the add-item endpoint.
    Future endpoints for listing, updating, and removing items are planned
    but not yet available.
"""
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
        """Test the connection to the API.
        
        Since the API only has add-item endpoint, we test by making a request
        with invalid data and checking if we get a proper API response (not a connection error).
        """
        try:
            # Try a minimal request to verify API is accessible and auth works
            # We expect this to fail validation but that proves the API is reachable
            url = f"{self.url}{API_ADD_ITEM}"
            headers = self._get_headers()
            
            async with self.session.request(
                "POST",
                url,
                headers=headers,
                json={},  # Empty data will fail validation but tests connectivity
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                # Any response (even 400) means API is reachable
                # 401 means auth failed (invalid API key)
                # 404 means endpoint doesn't exist
                if response.status == 401:
                    return False
                if response.status == 404:
                    return False
                # 400 or any other status means API is accessible
                return True
                
        except (asyncio.TimeoutError, ClientError):
            # Connection failed
            return False
        except Exception:  # pylint: disable=broad-except
            # Any other error means connection failed
            return False

    async def add_item(self, list_id: str, item_name: str) -> dict[str, Any]:
        """Add an item to a shopping list.
        
        Args:
            list_id: The ID of the shopping list (typically "default")
            item_name: The name of the item to add
            
        Returns:
            API response dictionary
            
        Raises:
            KoplistaAuthError: If API key is invalid (401)
            KoplistaApiError: If API request fails
            KoplistaConnectionError: If connection fails
        """
        data = {
            "listId": list_id,
            "itemName": item_name,
        }
        return await self._request("POST", API_ADD_ITEM, data)
