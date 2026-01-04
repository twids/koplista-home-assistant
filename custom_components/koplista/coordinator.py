"""Data update coordinator for Koplista."""
import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import KoplistaApiClient
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
        """Fetch data from API.
        
        Note: Currently only the add-item endpoint is implemented in the Koplista API.
        This coordinator returns an empty dict since there are no list/item fetch endpoints yet.
        """
        # Return empty data since only add_item endpoint exists
        return {}
