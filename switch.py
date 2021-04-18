#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Support for Tuya switches."""

import logging
from typing import Any, Dict, List, Optional, Tuple, cast

from homeassistant.core import HomeAssistant, Config
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.switch import (
    SwitchEntity,
)

from .const import (
    DOMAIN,
)

from .base import TuyaHaDevice

_LOGGER = logging.getLogger(__name__)


# Switch(kg), Socket(cz), Power Strip(pc)
# https://developer.tuya.com/docs/iot/open-api/standard-function/electrician-category/categorykgczpc?categoryId=486118
DPCODE_SWITCH = 'switch'


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    print('tuya.switch.async_setup_entry')

    haDevices = []
    for haDevice in hass.data[DOMAIN]['haDevices']:
        if haDevice.platform == 'switch':
            haDevices.append(haDevice)
    async_add_entities(haDevices)


class TuyaHaSwitch(TuyaHaDevice, SwitchEntity):
    """Tuya Switch Device."""

    platform = 'switch'

    # ToggleEntity

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self.tuyaDevice.status.get(DPCODE_SWITCH, False)

    def turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        self.tuyaDeviceManager.sendCommands(self.tuyaDevice.id, [{'code': DPCODE_SWITCH, 'value': True}])

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the device off."""
        self.tuyaDeviceManager.sendCommands(self.tuyaDevice.id, [{'code': DPCODE_SWITCH, 'value': False}])
