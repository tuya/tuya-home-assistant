#!/usr/bin/env python3
"""Support for Tuya switches."""
from __future__ import annotations

import logging
from typing import Any

from tuya_iot import TuyaHomeManager

from homeassistant.components.remote import RemoteEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .base import TuyaHaDevice
from .const import (
    DOMAIN,
    TUYA_HOME_MANAGER
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, _entry: ConfigEntry, async_add_entities
):
    """Set up tuya scenes."""
    _LOGGER.info("scenes remote init")

    entities = []

    scenes = await hass.async_add_executor_job(hass.data[DOMAIN][TUYA_HOME_MANAGER].query_scenes)
    for scene in scenes:
        entities.append(TuyaHAScene(scene))

    async_add_entities(entities)

class TuyaHAScene(TuyaHaDevice, RemoteEntity):
    """Tuya Scene Remote."""

    def __init__(self, scene) -> None:
        """Init Tuya Scene."""
        super().__init__()

        self.scene = scene
        self.entity_id = f"tuya_v2.ty{self.scene.scene_id}"

    @property
    def should_poll(self) -> bool:
        """Hass should not poll."""
        return False

    @property
    def unique_id(self) -> str | None:
        """Return a unique ID."""
        return f"tys{self.scene.scene_id}"

    @property
    def name(self) -> str | None:
        """Return Tuya scene name."""
        return self.scene.name

    @property
    def device_info(self):
        """Return a device description for device registry."""
        _device_info = {
            "identifiers": {(DOMAIN, f"{self.scene.scene_id}")},
            "manufacturer": "tuya",
            "name": self.scene.name,
            "model": "Tuya Scene",
        }
        return _device_info

    @property
    def available(self) -> bool:
        """Return if the scene is enabled."""
        return self.scene.enabled
