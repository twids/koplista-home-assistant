"""The Koplista integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import KoplistaApiClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Koplista from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    session = async_get_clientsession(hass)
    client = KoplistaApiClient(
        entry.data[CONF_URL],
        entry.data[CONF_API_KEY],
        session,
    )

    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
    }

    # Register services only once (for the first entry)
    if not hass.services.has_service(DOMAIN, "add_item"):
        from .services import async_setup_services

        await async_setup_services(hass)

    # Register intents only once (for the first entry)
    # Note: intent.async_register will not re-register if already registered
    from .intent import async_setup_intents

    async_setup_intents(hass)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)
    
    # Unregister services if this is the last entry
    remaining_entries = [
        e for e in hass.config_entries.async_entries(DOMAIN) if e.entry_id != entry.entry_id
    ]
    if not remaining_entries:
        from .const import SERVICE_ADD_ITEM
        
        hass.services.async_remove(DOMAIN, SERVICE_ADD_ITEM)

    return True
