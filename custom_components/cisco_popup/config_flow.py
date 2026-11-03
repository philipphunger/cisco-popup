"""Configure one Cisco popup phone through the UI."""
from ipaddress import IPv4Address

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector

from . import DOMAIN


class CiscoPopupConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        errors = {}
        if user_input is not None:
            try:
                user_input["host"] = str(IPv4Address(user_input["host"].strip()))
            except ValueError:
                errors["host"] = "invalid_host"
            else:
                return self.async_create_entry(
                    title=f"Cisco Popup ({user_input['host']})", data=user_input
                )
        defaults = user_input or {}
        return self.async_show_form(
            step_id="user", errors=errors,
            data_schema=vol.Schema({
                vol.Required("host", default=defaults.get("host", "")): str,
                vol.Required("username", default=defaults.get("username", "")): str,
                vol.Required("password", default=defaults.get("password", "")):
                    selector.TextSelector(selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)),
            }),
        )
