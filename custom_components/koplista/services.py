"""Services for Koplista integration."""
import logging

import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, SERVICE_ADD_ITEM

_LOGGER = logging.getLogger(__name__)

SERVICE_ADD_ITEM_SCHEMA = vol.Schema(
    {
        vol.Optional("list_id"): cv.string,
        vol.Required("item"): cv.string,
    }
)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for Koplista."""

    async def async_add_item(call: ServiceCall) -> None:
        """Handle add item service call.
        
        Note: Only the add_item service is available since the Koplista API
        currently only implements the add-item endpoint.
        """
        list_id = call.data.get("list_id", "default")
        item_name = call.data.get("item")
        
        if not item_name:
            _LOGGER.error("Item name is required")
            return

        # Get the first entry (assumes single integration instance)
        # Limitation: Multiple instances not supported
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            _LOGGER.error("No Koplista integration configured")
            return

        entry = entries[0]
        client = hass.data[DOMAIN][entry.entry_id]["client"]

        try:
            await client.add_item(list_id, item_name)
            _LOGGER.info("Added item '%s' to list '%s'", item_name, list_id)
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Failed to add item: %s", err)

    # Register service only if not already registered
    if not hass.services.has_service(DOMAIN, SERVICE_ADD_ITEM):
        hass.services.async_register(
            DOMAIN,
            SERVICE_ADD_ITEM,
            async_add_item,
            schema=SERVICE_ADD_ITEM_SCHEMA,
        )
