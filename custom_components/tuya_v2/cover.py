#!/usr/bin/env python3
"""Support for Tuya Cover."""
from __future__ import annotations

import logging
from typing import Any, List

from homeassistant.components.cover import (
    DEVICE_CLASS_CURTAIN,
    DOMAIN as DEVICE_DOMAIN,
    SUPPORT_CLOSE,
    SUPPORT_OPEN,
    SUPPORT_SET_POSITION,
    SUPPORT_STOP,
    CoverEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .base import TuyaHaDevice
from .const import DOMAIN, TUYA_DEVICE_MANAGER, TUYA_DISCOVERY_NEW, TUYA_HA_TUYA_MAP, TUYA_HA_DEVICES

_LOGGER = logging.getLogger(__name__)

TUYA_SUPPORT_TYPE = {"cl", "clkg"}  # Curtain  # Curtain Switch

# Curtain
# https://developer.tuya.com/en/docs/iot/f?id=K9gf46o5mtfyc
DPCODE_CONTROL = "control"
DPCODE_PERCENT_CONTROL = "percent_control"
DPCODE_PERCENT_STATE = "percent_state"

ATTR_POSITION = "position"


async def async_setup_entry(
    hass: HomeAssistant, _entry: ConfigEntry, async_add_entities
):
    """Set up tuya cover dynamically through tuya discovery."""
    _LOGGER.info("cover init")

    hass.data[DOMAIN][TUYA_HA_TUYA_MAP].update({DEVICE_DOMAIN: TUYA_SUPPORT_TYPE})

    async def async_discover_device(dev_ids):
        """Discover and add a discovered tuya cover."""
        _LOGGER.info(f"cover add-> {dev_ids}")
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
    """Set up Tuya Cover."""
    device_manager = hass.data[DOMAIN][TUYA_DEVICE_MANAGER]
    entities = []
    for device_id in device_ids:
        device = device_manager.device_map[device_id]
        if device is None:
            continue
        entities.append(TuyaHaCover(device, device_manager))
    return entities


class TuyaHaCover(TuyaHaDevice, CoverEntity):
    """Tuya Switch Device."""

    # property
    @property
    def device_class(self) -> str:
        """Return Entity Properties."""
        return DEVICE_CLASS_CURTAIN

    @property
    def is_closed(self) -> bool | None:
        return False

    @property
    def current_cover_position(self) -> int:
        """Return cover current position."""
        position = self.tuya_device.status.get(DPCODE_PERCENT_STATE, 0)
        return 100 - position

    def open_cover(self, **kwargs: Any) -> None:
        """Open the cover."""
        self._send_command([{"code": DPCODE_CONTROL, "value": "open"}])

    def close_cover(self, **kwargs: Any) -> None:
        """Close cover."""
        self._send_command([{"code": DPCODE_CONTROL, "value": "close"}])

    def stop_cover(self, **kwargs):
        """Stop the cover."""
        self._send_command([{"code": DPCODE_CONTROL, "value": "stop"}])

    def set_cover_position(self, **kwargs):
        """Move the cover to a specific position."""
        _LOGGER.debug(f"cover--> {kwargs}")
        self._send_command(
            [{"code": DPCODE_PERCENT_CONTROL, "value": kwargs[ATTR_POSITION]}]
        )

    @property
    def supported_features(self):
        """Flag supported features."""
        supports = SUPPORT_OPEN | SUPPORT_CLOSE | SUPPORT_STOP

        if DPCODE_PERCENT_CONTROL in self.tuya_device.status:
            supports = supports | SUPPORT_SET_POSITION

        return supports
