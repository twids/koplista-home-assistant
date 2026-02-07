"""Intent handlers for Koplista."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent

from .api import KoplistaApiError, KoplistaConnectionError
from .const import DOMAIN, INTENT_ADD_ITEM

_LOGGER = logging.getLogger(__name__)


class AddItemIntentHandler(intent.IntentHandler):
    """Handle AddItem intents."""

    intent_type = INTENT_ADD_ITEM

    async def async_handle(self, intent_obj: intent.Intent) -> intent.IntentResponse:
        """Handle the intent."""
        hass = intent_obj.hass
        item_name = intent_obj.slots.get("item", {}).get("value")
        list_id = intent_obj.slots.get("list_id", {}).get("value", "default")

        # Detect language from conversation agent (defaults to Swedish)
        language = intent_obj.language or "sv"
        is_swedish = language.startswith("sv")

        if not item_name:
            response = intent_obj.create_response()
            speech = "Jag hörde inte vad som skulle läggas till" if is_swedish else "I didn't catch the item name"
            response.async_set_speech(speech)
            return response

        # Get the first entry (assumes single integration instance)
        # Limitation: Multiple instances not supported
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            response = intent_obj.create_response()
            speech = "Koplista är inte konfigurerad" if is_swedish else "Koplista integration is not configured"
            response.async_set_speech(speech)
            return response

        entry = entries[0]
        client = hass.data[DOMAIN][entry.entry_id]["client"]

        try:
            await client.add_item(list_id, item_name)

            response = intent_obj.create_response()
            if is_swedish:
                speech = f"Lagt till {item_name} på koplista"
            else:
                speech = f"Added {item_name} to the shopping list"
            response.async_set_speech(speech)
            _LOGGER.info("Added item '%s' via intent", item_name)
            return response

        except (KoplistaApiError, KoplistaConnectionError) as err:
            _LOGGER.error("Error adding item via intent: %s", err)
            response = intent_obj.create_response()
            if is_swedish:
                speech = f"Kunde inte lägga till {item_name} på koplista"
            else:
                speech = f"Failed to add {item_name} to the shopping list"
            response.async_set_speech(speech)
            return response


def async_setup_intents(hass: HomeAssistant) -> None:
    """Set up intent handlers."""
    intent.async_register(hass, AddItemIntentHandler())
