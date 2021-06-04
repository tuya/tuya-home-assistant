#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Support for Tuya switches."""

import json
import logging
from typing import Any, Dict, List, Optional, Tuple, cast
from tuya_iot import TuyaDeviceManager, TuyaDevice

from homeassistant.core import HomeAssistant, Config
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.number import (
    NumberEntity,
    DOMAIN as DEVICE_DOMAIN
)
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect
)

from .const import (
    DOMAIN,
    TUYA_HA_TUYA_MAP,
    TUYA_DISCOVERY_NEW,
    TUYA_DEVICE_MANAGER,
    TUYA_HA_DEVICES
)

from .base import TuyaHaDevice

_LOGGER = logging.getLogger(__name__)

TUYA_SUPPORT_TYPE = {
    "hps",    # Human Presence Sensor
}

# Switch(kg), Socket(cz), Power Strip(pc)
# https://developer.tuya.com/docs/iot/open-api/standard-function/electrician-category/categorykgczpc?categoryId=486118
DPCODE_SENSITIVITY = 'sensitivity'

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up tuya number dynamically through tuya discovery."""
    print("switch init")

    hass.data[DOMAIN][TUYA_HA_TUYA_MAP].update({DEVICE_DOMAIN: TUYA_SUPPORT_TYPE})

    # platform = config_entry.data[CONF_PLATFORM]

    async def async_discover_device(dev_ids):
        """Discover and add a discovered tuya number."""
        print("switch add->", dev_ids)
        if not dev_ids:
            return
        entities = await hass.async_add_executor_job(
            _setup_entities,
            hass,
            dev_ids
        )
        hass.data[DOMAIN][TUYA_HA_DEVICES].extend(entities)
        async_add_entities(entities)

    async_dispatcher_connect(
        hass, TUYA_DISCOVERY_NEW.format(DEVICE_DOMAIN), async_discover_device
    )

    device_manager = hass.data[DOMAIN][TUYA_DEVICE_MANAGER]
    device_ids = []
    for (device_id, device) in device_manager.deviceMap.items():
        if device.category in TUYA_SUPPORT_TYPE:
            device_ids.append(device_id)
    await async_discover_device(device_ids)


def _setup_entities(hass, device_ids: List):
    """Set up Tuya Switch device."""
    device_manager = hass.data[DOMAIN][TUYA_DEVICE_MANAGER]
    entities = []
    for device_id in device_ids:
        device = device_manager.deviceMap[device_id]
        if device is None:
            continue

        if DPCODE_SENSITIVITY in device.status:
            entities.append(TuyaHaNumber(device, device_manager, DPCODE_SENSITIVITY))
        
        
    return entities

class TuyaHaNumber(TuyaHaDevice, NumberEntity):
    """Tuya Device Number."""

    platform = 'number'

    def __init__(self, device: TuyaDevice, 
                deviceManager: TuyaDeviceManager, 
                code:str = ''):
        super().__init__(device, deviceManager)
        self._code = code
            
    # ToggleEntity

    def set_value(self, value: float) -> None:
        """Update the current value."""
        self.tuyaDeviceManager.sendCommands(self.tuyaDevice.id, [{'code': self._code, 'value': int(value)}])

    @property
    def unique_id(self) -> Optional[str]:
        """Return a unique ID."""
        return self.tuyaDevice.uuid + self._code

    @property
    def value(self) -> float:
        """Return current value."""
        return self.tuyaDevice.status.get(self._code, 0)
    
    @property
    def min_value(self) -> float:
        return self._get_code_range()[0]
    
    @property
    def max_value(self) -> float:
        return self._get_code_range()[1]
    
    @property
    def step(self) -> float:
        return self._get_code_range()[2]

    def _get_code_range(self) -> Tuple[int, int, int]:
        range = json.loads(self.tuyaDevice.function.get(self._code).values)
        return range.get('min',0), range.get('max',0), range.get('step',0)
