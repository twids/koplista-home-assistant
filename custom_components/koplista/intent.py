"""Intent handlers for Koplista."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent

from .const import DOMAIN, INTENT_ADD_ITEM

_LOGGER = logging.getLogger(__name__)


class AddItemIntentHandler(intent.IntentHandler):
    """Handle AddItem intents."""

    intent_type = INTENT_ADD_ITEM

    async def async_handle(self, intent_obj: intent.Intent) -> intent.IntentResponse:
        """Handle the intent."""
        hass = intent_obj.hass
        item_name = intent_obj.slots.get("item", {}).get("value")

        if not item_name:
            response = intent_obj.create_response()
            response.async_set_speech("I didn't catch the item name")
            return response

        # Get the first entry (assumes single integration instance)
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            response = intent_obj.create_response()
            response.async_set_speech("Koplista integration is not configured")
            return response

        entry = entries[0]
        coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
        client = hass.data[DOMAIN][entry.entry_id]["client"]

        # Use the first list as default
        list_id = next(iter(coordinator.data.keys()), None)

        if list_id is None:
            response = intent_obj.create_response()
            response.async_set_speech("No shopping lists found")
            return response

        try:
            await client.add_item(list_id, item_name)
            await coordinator.async_request_refresh()

            response = intent_obj.create_response()
            response.async_set_speech(f"Added {item_name} to the shopping list")
            _LOGGER.info("Added item '%s' via intent", item_name)
            return response

        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Error adding item via intent: %s", err)
            response = intent_obj.create_response()
            response.async_set_speech(f"Failed to add {item_name} to the shopping list")
            return response


def async_setup_intents(hass: HomeAssistant) -> None:
    """Set up intent handlers."""
    intent.async_register(hass, AddItemIntentHandler())
