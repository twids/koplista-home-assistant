"""Config flow for Koplista integration."""
import logging
from typing import Any

import voluptuous as vol
from aiohttp import ClientError
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import KoplistaApiClient, KoplistaApiError, KoplistaConnectionError
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL): str,
        vol.Required(CONF_API_KEY): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    session = async_get_clientsession(hass)
    client = KoplistaApiClient(data[CONF_URL], data[CONF_API_KEY], session)

    if not await client.test_connection():
        raise KoplistaApiError("Cannot connect to Koplista")

    return {"title": "Koplista"}


class KoplistaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Koplista."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except (KoplistaApiError, KoplistaConnectionError):
                errors["base"] = "cannot_connect"
            except ClientError:
                _LOGGER.exception("Connection error")
                errors["base"] = "cannot_connect"
            except ValueError as err:
                _LOGGER.error("Invalid configuration: %s", err)
                errors["base"] = "invalid_url"
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception during setup: %s", err)
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle reconfiguration of the integration."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                await validate_input(self.hass, user_input)
            except (KoplistaApiError, KoplistaConnectionError):
                errors["base"] = "cannot_connect"
            except ClientError:
                _LOGGER.exception("Connection error")
                errors["base"] = "cannot_connect"
            except ValueError as err:
                _LOGGER.error("Invalid configuration: %s", err)
                errors["base"] = "invalid_url"
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception during reconfiguration: %s", err)
                errors["base"] = "unknown"
            else:
                # Update the entry and reload the integration
                return self.async_update_reload_and_abort(
                    self._get_reconfigure_entry(),
                    data=user_input,
                )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
