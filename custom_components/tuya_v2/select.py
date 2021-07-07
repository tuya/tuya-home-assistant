#!/usr/bin/env python3
"""Support for Tuya Mode Sensor."""

import json
import logging
from typing import List

from tuya_iot import TuyaDevice, TuyaDeviceManager

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.select import DOMAIN as DEVICE_DOMAIN, SelectEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .base import TuyaHaDevice

from .const import (
    DOMAIN,
    TUYA_DEVICE_MANAGER,
    TUYA_DISCOVERY_NEW,
    TUYA_HA_DEVICES,
    TUYA_HA_TUYA_MAP,
)

_LOGGER = logging.getLogger(__name__)

TUYA_SUPPORT_TYPE = {
    "xxj"
}

DPCODE_MODE = "mode"

async def async_setup_entry(hass: HomeAssistant, _entry: ConfigEntry, async_add_entities):
    _LOGGER.info("select init")

    hass.data[DOMAIN][TUYA_HA_TUYA_MAP].update({DEVICE_DOMAIN: TUYA_SUPPORT_TYPE})

    async def async_discover_device(dev_ids):
        _LOGGER.info(f"select add-> {dev_ids}")
        if not dev_ids:
            return
        entities = await hass.async_add_executor_job(_setup_entities, hass, dev_ids)
        hass.data[DOMAIN][TUYA_HA_DEVICES].extend(entities)
        async_add_entities(entities)

    async_dispatcher_connect(
        hass, TUYA_DISCOVERY_NEW.format(DEVICE_DOMAIN), async_discover_device
    )

    device_manager = hass.data[DOMAIN][TUYA_DEVICE_MANAGER]
    device_ids = []
    for (device_id, device) in device_manager.device_map.items():
        if device.category in TUYA_SUPPORT_TYPE:
            device_ids.append(device_id)
    await async_discover_device(device_ids)


def _setup_entities(hass, device_ids: List):
    device_manager = hass.data[DOMAIN][TUYA_DEVICE_MANAGER]
    entities = []
    for device_id in device_ids:
        device = device_manager.device_map[device_id]
        if device is None:
            continue

        if DPCODE_MODE in device.status:
            entities.append(TuyaHaSelect(device, device_manager, DPCODE_MODE))

    return entities

class TuyaHaSelect(TuyaHaDevice, SelectEntity):
    def __init__(self, device: TuyaDevice, device_manager: TuyaDeviceManager, code: str = ""):
        self._code = code
        self._attr_current_option = None
        super().__init__(device, device_manager)

    @property
    def current_option(self) -> str:
        return self.tuya_device.status.get(self._code, None)

    def select_option(self, option: str) -> None:
        self._send_command([{"code": self._code, "value": option}])        

    @property
    def options(self) -> List:
        dp_range = json.loads(self.tuya_device.function.get(self._code).values)
        return dp_range.get("range",[])
    
