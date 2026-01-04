"""Services for Koplista integration."""
import logging
from typing import Any

import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, SERVICE_ADD_ITEM, SERVICE_REMOVE_ITEM

_LOGGER = logging.getLogger(__name__)

SERVICE_ADD_ITEM_SCHEMA = vol.Schema(
    {
        vol.Optional("list_name"): cv.string,
        vol.Required("item"): cv.string,
    }
)

SERVICE_REMOVE_ITEM_SCHEMA = vol.Schema(
    {
        vol.Optional("list_name"): cv.string,
        vol.Required("item"): cv.string,
    }
)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for Koplista."""

    async def async_add_item(call: ServiceCall) -> None:
        """Handle add item service call."""
        list_name = call.data.get("list_name")
        item_name = call.data["item"]

        # Get the first entry (assumes single integration instance)
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            _LOGGER.error("No Koplista integration configured")
            return

        entry = entries[0]
        coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
        client = hass.data[DOMAIN][entry.entry_id]["client"]

        # Find the list to add to
        list_id = None
        if list_name:
            for lid, list_data in coordinator.data.items():
                if list_data.get("info", {}).get("name", "").lower() == list_name.lower():
                    list_id = lid
                    break
        else:
            # Use the first list as default
            list_id = next(iter(coordinator.data.keys()), None)

        if list_id is None:
            _LOGGER.error("Shopping list not found: %s", list_name)
            return

        await client.add_item(list_id, item_name)
        await coordinator.async_request_refresh()
        _LOGGER.info("Added item '%s' to list '%s'", item_name, list_name or "default")

    async def async_remove_item(call: ServiceCall) -> None:
        """Handle remove item service call."""
        list_name = call.data.get("list_name")
        item_name = call.data["item"]

        # Get the first entry (assumes single integration instance)
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            _LOGGER.error("No Koplista integration configured")
            return

        entry = entries[0]
        coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
        client = hass.data[DOMAIN][entry.entry_id]["client"]

        # Find the list and item
        item_id = None
        if list_name:
            for lid, list_data in coordinator.data.items():
                if list_data.get("info", {}).get("name", "").lower() == list_name.lower():
                    for item in list_data.get("items", []):
                        if item.get("name", "").lower() == item_name.lower():
                            item_id = item.get("id")
                            break
                    break
        else:
            # Search all lists
            for list_data in coordinator.data.values():
                for item in list_data.get("items", []):
                    if item.get("name", "").lower() == item_name.lower():
                        item_id = item.get("id")
                        break
                if item_id:
                    break

        if item_id is None:
            _LOGGER.error("Item not found: %s", item_name)
            return

        await client.remove_item(item_id)
        await coordinator.async_request_refresh()
        _LOGGER.info("Removed item '%s' from list", item_name)

    # Register services only if not already registered
    if not hass.services.has_service(DOMAIN, SERVICE_ADD_ITEM):
        hass.services.async_register(
            DOMAIN,
            SERVICE_ADD_ITEM,
            async_add_item,
            schema=SERVICE_ADD_ITEM_SCHEMA,
        )

    if not hass.services.has_service(DOMAIN, SERVICE_REMOVE_ITEM):
        hass.services.async_register(
            DOMAIN,
            SERVICE_REMOVE_ITEM,
            async_remove_item,
            schema=SERVICE_REMOVE_ITEM_SCHEMA,
        )
