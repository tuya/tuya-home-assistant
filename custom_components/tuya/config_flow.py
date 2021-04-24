#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Config flow for Tuya."""

import logging
import voluptuous as vol

from homeassistant import config_entries

from .const import (
    DOMAIN,
    CONF_ENDPOINT,
    CONF_ACCESS_ID,
    CONF_ACCESS_SECRET,
    CONF_USERNAME,
    CONF_PASSWORD,
)

from tuya_iot import TuyaOpenAPI
RESULT_SINGLE_INSTANCE = "single_instance_allowed"

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA_USER = vol.Schema(
    {
        vol.Required(CONF_ENDPOINT): str,
        vol.Required(CONF_ACCESS_ID): str,
        vol.Required(CONF_ACCESS_SECRET): str,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)

class TuyaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    def _try_login(self, user_input):
        print('TuyaConfigFlow._try_login start, user_input:', user_input)

        api = TuyaOpenAPI(user_input[CONF_ENDPOINT], user_input[CONF_ACCESS_ID], user_input[CONF_ACCESS_SECRET])
        api.set_dev_channel('hass')
        response = api.login(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])

        print('TuyaConfigFlow._try_login finish, response:', response)
        return response

    async def async_step_import(self, user_input=None):
        return await self.async_step_user(user_input, is_import=True)

    async def async_step_user(self, user_input=None, is_import=False):
        print('TuyaConfigFlow.async_step_user start, is_import=', is_import)
        
        if self._async_current_entries():
            return self.async_abort(reason=RESULT_SINGLE_INSTANCE)

        errors = {}
        if user_input is not None:
            response = await self.hass.async_add_executor_job(self._try_login, user_input)
            if response.get('success', False):
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME],
                    data=user_input,
                )
            else:
                errors['base'] = 'code={}, msg={}'.format(response.get('code', 0), response.get('msg', ''))
                if is_import == True:
                    return self.async_abort(reason=errors['base'])

        return self.async_show_form(
            step_id='user',
            data_schema=DATA_SCHEMA_USER,
            errors=errors,
        )
