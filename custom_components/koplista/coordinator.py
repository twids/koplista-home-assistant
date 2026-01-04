"""Data update coordinator for Koplista."""
import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import KoplistaApiClient, KoplistaApiError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class KoplistaDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Koplista data."""

    def __init__(self, hass: HomeAssistant, client: KoplistaApiClient) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.client = client

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        try:
            lists = await self.client.get_lists()
            data = {}

            for shopping_list in lists:
                list_id = shopping_list["id"]
                items = await self.client.get_items(list_id)
                data[list_id] = {
                    "info": shopping_list,
                    "items": items,
                }

            return data

        except KoplistaApiError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
