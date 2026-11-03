"""Cisco phone popup action."""
import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .client import PopupError, send_popup

DOMAIN = "cisco_popup"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Register actions even when no phone is loaded."""
    hass.data.setdefault(DOMAIN, {})

    async def handle_send(call: ServiceCall) -> None:
        entries = hass.data[DOMAIN]
        if not entries:
            raise HomeAssistantError("Cisco Popup zuerst unter Geraete & Dienste einrichten.")
        data = next(iter(entries.values()))
        try:
            await send_popup(
                async_get_clientsession(hass), data["host"],
                data["username"], data["password"],
                call.data["title"], call.data["message"],
            )
        except PopupError as err:
            raise HomeAssistantError(str(err)) from err

    hass.services.async_register(
        DOMAIN, "send_message", handle_send,
        schema=vol.Schema({
            vol.Required("message"): vol.All(cv.string, vol.Length(min=1, max=4000)),
            vol.Optional("title", default="Home Assistant"): vol.All(cv.string, vol.Length(max=100)),
        }),
    )
    return True


async def async_setup_entry(hass, entry) -> bool:
    hass.data[DOMAIN][entry.entry_id] = dict(entry.data)
    return True


async def async_unload_entry(hass, entry) -> bool:
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True
