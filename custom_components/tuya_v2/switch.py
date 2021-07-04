#!/usr/bin/env python3
"""Support for Tuya switches."""
from __future__ import annotations

import logging
from typing import Any

from tuya_iot import TuyaDevice, TuyaDeviceManager

from homeassistant.components.switch import DOMAIN as DEVICE_DOMAIN, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
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
    "kg",  # Switch
    "cz",  # Socket
    "pc",  # Power Strip
    "cwysj",  # Pet Water Feeder
    "dlq",  # Breaker
}

# Switch(kg), Socket(cz), Power Strip(pc)
# https://developer.tuya.com/docs/iot/open-api/standard-function/electrician-category/categorykgczpc?categoryId=486118
DPCODE_SWITCH = "switch"
DPCODE_UV = "uv"


async def async_setup_entry(
    hass: HomeAssistant, _entry: ConfigEntry, async_add_entities
):
    """Set up tuya sensors dynamically through tuya discovery."""
    _LOGGER.info("switch init")

    hass.data[DOMAIN][TUYA_HA_TUYA_MAP].update({DEVICE_DOMAIN: TUYA_SUPPORT_TYPE})

    async def async_discover_device(dev_ids):
        """Discover and add a discovered tuya sensor."""
        _LOGGER.info(f"switch add-> {dev_ids}")
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


def _setup_entities(hass, device_ids: list):
    """Set up Tuya Switch device."""
    device_manager = hass.data[DOMAIN][TUYA_DEVICE_MANAGER]
    entities = []
    for device_id in device_ids:
        device = device_manager.device_map[device_id]
        if device is None:
            continue

        for function in device.function:
            if function.startswith(DPCODE_SWITCH):
                entities.append(TuyaHaSwitch(device, device_manager, function))
                continue

            if function == DPCODE_UV:
                entities.append(TuyaHaSwitch(device, device_manager, function))

    return entities


class TuyaHaSwitch(TuyaHaDevice, SwitchEntity):
    """Tuya Switch Device."""

    dp_code_switch = DPCODE_SWITCH

    def __init__(
        self, device: TuyaDevice, device_manager: TuyaDeviceManager, dp_code: str = ""
    ) -> None:
        """Init TuyaHaSwitch."""
        super().__init__(device, device_manager)

        self.dp_code = dp_code
        self.channel = (
            dp_code.replace(DPCODE_SWITCH, "")
            if dp_code.startswith(DPCODE_SWITCH)
            else dp_code
        )

    @property
    def unique_id(self) -> str | None:
        """Return a unique ID."""
        return f"{super().unique_id}{self.channel}"

    @property
    def name(self) -> str | None:
        """Return Tuya device name."""
        return self.tuya_device.name + self.channel

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self.tuya_device.status.get(self.dp_code, False)

    def turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        self._send_command([{"code": self.dp_code, "value": True}])

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the device off."""
        self._send_command([{"code": self.dp_code, "value": False}])
