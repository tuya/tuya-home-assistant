"""Support for Tuya Remotes."""
from __future__ import annotations

import logging
from collections.abc import Iterable
from typing import Any

from homeassistant.components.remote import RemoteEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from tuya_iot import TuyaHomeManager, TuyaRemote, TuyaDevice, TuyaDeviceManager

from .base import TuyaHaDevice
from .const import (
    DOMAIN,
    TUYA_HOME_MANAGER,
    TUYA_DEVICE_MANAGER
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant, _entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    _LOGGER.info("remote init")

    __device_manager = hass.data[DOMAIN][TUYA_DEVICE_MANAGER]
    __home_manager = hass.data[DOMAIN][TUYA_HOME_MANAGER]
    remotes = await hass.async_add_executor_job(__home_manager.query_infrared_devices)

    entities = []
    for remote in remotes:
        _LOGGER.info(f"remote add-> {remote.remote_id}")
        entities.append(TuyaHARemote(__device_manager.device_map[remote.remote_id], __device_manager, __home_manager, remote))

    async_add_entities(entities)


class TuyaHARemote(TuyaHaDevice, RemoteEntity):
    def __init__(self, device: TuyaDevice, device_manager: TuyaDeviceManager, home_manager: TuyaHomeManager, remote: TuyaRemote) -> None:
        self.home_manager = home_manager
        self.remote = remote
        super().__init__(device, device_manager)

    def send_command(self, command: Iterable[str], **kwargs: Any) -> None:
        if not (any(x.remote_name == kwargs["device"] for x in self.remote.remote_devices)):
            _LOGGER.warn("Command not found in your tuya platform %s", kwargs["device"])
            return

        for cmd in command:
            device_id = next(x.remote_id for x in self.remote.remote_devices if x.remote_name == kwargs["device"])
            self.home_manager.trigger_infrared_commands(self.remote.remote_id, device_id, cmd)
