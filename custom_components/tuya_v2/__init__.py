#!/usr/bin/env python3
"""Support for Tuya Smart devices."""

import itertools
import json
import logging
from .aes_cbc import (
    AesCBC as Aes,
    XOR_KEY,
    KEY_KEY,
    AES_ACCOUNT_KEY,
)
from typing import Any

from tuya_iot import (
    ProjectType,
    TuyaDevice,
    TuyaDeviceListener,
    TuyaDeviceManager,
    TuyaHomeManager,
    TuyaOpenAPI,
    TuyaOpenMQ,
    tuya_logger,
)
import voluptuous as vol

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import (
    CONF_ACCESS_ID,
    CONF_ACCESS_SECRET,
    CONF_APP_TYPE,
    CONF_COUNTRY_CODE,
    CONF_ENDPOINT,
    CONF_PASSWORD,
    CONF_PROJECT_TYPE,
    CONF_USERNAME,
    DOMAIN,
    TUYA_DEVICE_MANAGER,
    TUYA_DISCOVERY_NEW,
    TUYA_HA_DEVICES,
    TUYA_HA_TUYA_MAP,
    TUYA_HOME_MANAGER,
    TUYA_MQTT_LISTENER,
    TUYA_SETUP_PLATFORM,
    TUYA_SUPPORT_HA_TYPE,
)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    vol.All(
        cv.deprecated(DOMAIN),
        {
            DOMAIN: vol.Schema(
                {
                    vol.Required(CONF_PROJECT_TYPE): int,
                    vol.Required(CONF_ENDPOINT): cv.string,
                    vol.Required(CONF_ACCESS_ID): cv.string,
                    vol.Required(CONF_ACCESS_SECRET): cv.string,
                    CONF_USERNAME: cv.string,
                    CONF_PASSWORD: cv.string,
                    CONF_COUNTRY_CODE: cv.string,
                    CONF_APP_TYPE: cv.string,
                }
            )
        },
    ),
    extra=vol.ALLOW_EXTRA,
)

# decrypt or encrypt entry info


def entry_decrypt(hass: HomeAssistant, entry: ConfigEntry, init_entry_data):
    aes = Aes()
    # decrypt the new account info
    if XOR_KEY in init_entry_data:
        _LOGGER.info("tuya.__init__.exist_xor_cache-->True")
        key_iv = aes.xor_decrypt(init_entry_data[XOR_KEY], init_entry_data[KEY_KEY])
        cbc_key = key_iv[0:16]
        cbc_iv = key_iv[16:32]
        decrpyt_str = aes.cbc_decrypt(
            cbc_key, cbc_iv, init_entry_data[AES_ACCOUNT_KEY]
        )
        # _LOGGER.info(f"tuya.__init__.exist_xor_cache:::decrpyt_str-->{decrpyt_str}")
        entry_data = aes.json_to_dict(decrpyt_str)
    else:
        # if not exist xor cache, use old account info
        _LOGGER.info("tuya.__init__.exist_xor_cache-->False")
        entry_data = init_entry_data
        cbc_key = aes.random_16()
        cbc_iv = aes.random_16()
        access_id = init_entry_data[CONF_ACCESS_ID]
        access_id_entry = aes.cbc_encrypt(cbc_key, cbc_iv, access_id)
        c = cbc_key + cbc_iv
        c_xor_entry = aes.xor_encrypt(c, access_id_entry)
        # account info encrypted with AES-CBC
        user_input_encrpt = aes.cbc_encrypt(cbc_key, cbc_iv, json.dumps(dict(init_entry_data)))
        # udpate old account info
        hass.config_entries.async_update_entry(
            entry,
            data={
                AES_ACCOUNT_KEY: user_input_encrpt,
                XOR_KEY: c_xor_entry,
                KEY_KEY: access_id_entry,
            },
        )
    return entry_data


async def _init_tuya_sdk(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    init_entry_data = entry.data
    # decrypt or encrypt entry info
    entry_data = entry_decrypt(hass, entry, init_entry_data)
    project_type = ProjectType(entry_data[CONF_PROJECT_TYPE])
    api = TuyaOpenAPI(
        entry_data[CONF_ENDPOINT],
        entry_data[CONF_ACCESS_ID],
        entry_data[CONF_ACCESS_SECRET],
        project_type,
    )

    api.set_dev_channel("hass")

    response = (
        await hass.async_add_executor_job(
            api.login, entry_data[CONF_USERNAME], entry_data[CONF_PASSWORD]
        )
        if project_type == ProjectType.INDUSTY_SOLUTIONS
        else await hass.async_add_executor_job(
            api.login,
            entry_data[CONF_USERNAME],
            entry_data[CONF_PASSWORD],
            entry_data[CONF_COUNTRY_CODE],
            entry_data[CONF_APP_TYPE],
        )
    )
    if response.get("success", False) is False:
        _LOGGER.error(f"Tuya login error response: {response}")
        return False

    tuya_mq = TuyaOpenMQ(api)
    tuya_mq.start()

    device_manager = TuyaDeviceManager(api, tuya_mq)

    # Get device list
    home_manager = TuyaHomeManager(api, tuya_mq, device_manager)
    await hass.async_add_executor_job(home_manager.update_device_cache)
    hass.data[DOMAIN][TUYA_HOME_MANAGER] = home_manager

    class DeviceListener(TuyaDeviceListener):
        """Device Update Listener."""

        def update_device(self, device: TuyaDevice):
            for ha_device in hass.data[DOMAIN][TUYA_HA_DEVICES]:
                if ha_device.tuya_device.id == device.id:
                    _LOGGER.debug(f"_update-->{self};->>{ha_device.tuya_device.status}")
                    ha_device.schedule_update_ha_state()

        def add_device(self, device: TuyaDevice):

            device_add = False

            _LOGGER.info(
                f"""add device category->{device.category}; keys->,
                {hass.data[DOMAIN][TUYA_HA_TUYA_MAP].keys()}"""
            )
            if device.category in itertools.chain(
                *hass.data[DOMAIN][TUYA_HA_TUYA_MAP].values()
            ):
                ha_tuya_map = hass.data[DOMAIN][TUYA_HA_TUYA_MAP]

                remove_hass_device(hass, device.id)

                for key, tuya_list in ha_tuya_map.items():
                    if device.category in tuya_list:
                        device_add = True
                        async_dispatcher_send(
                            hass, TUYA_DISCOVERY_NEW.format(key), [device.id]
                        )

            if device_add:
                device_manager = hass.data[DOMAIN][TUYA_DEVICE_MANAGER]
                device_manager.mq.stop()
                tuya_mq = TuyaOpenMQ(device_manager.api)
                tuya_mq.start()

                device_manager.mq = tuya_mq
                tuya_mq.add_message_listener(device_manager._on_message)

        def remove_device(self, device_id: str):
            _LOGGER.info(f"tuya remove device:{device_id}")
            remove_hass_device(hass, device_id)

    __listener = DeviceListener()
    hass.data[DOMAIN][TUYA_MQTT_LISTENER] = __listener
    device_manager.add_device_listener(__listener)
    hass.data[DOMAIN][TUYA_DEVICE_MANAGER] = device_manager

    # Clean up device entities
    await cleanup_device_registry(hass)

    _LOGGER.info(f"init support type->{TUYA_SUPPORT_HA_TYPE}")

    for platform in TUYA_SUPPORT_HA_TYPE:
        _LOGGER.info(f"tuya async platform-->{platform}")
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
        hass.data[DOMAIN][TUYA_SETUP_PLATFORM].add(platform)

    return True


async def cleanup_device_registry(hass: HomeAssistant):
    """Remove deleted device registry entry if there are no remaining entities."""

    device_registry = hass.helpers.device_registry.async_get(hass)
    device_manager = hass.data[DOMAIN][TUYA_DEVICE_MANAGER]

    for dev_id, device_entity in list(device_registry.devices.items()):
        for item in device_entity.identifiers:
            if DOMAIN == item[0] and item[1] not in device_manager.device_map.keys():
                device_registry.async_remove_device(dev_id)
                break


def remove_hass_device(hass: HomeAssistant, device_id: str):
    """Remove device from hass cache."""
    device_registry = hass.helpers.device_registry.async_get(hass)
    entity_registry = hass.helpers.entity_registry.async_get(hass)
    for entity in list(entity_registry.entities.values()):
        if entity.unique_id.startswith(f"ty{device_id}"):
            entity_registry.async_remove(entity.entity_id)
            if device_registry.async_get(entity.device_id):
                device_registry.async_remove_device(entity.device_id)


async def async_setup(hass, config):
    """Set up the Tuya integration."""
    tuya_logger.setLevel(_LOGGER.level)
    conf = config.get(DOMAIN)

    _LOGGER.info(f"Tuya async setup conf {conf}")
    if conf is not None:

        async def flow_init() -> Any:
            try:
                result = await hass.config_entries.flow.async_init(
                    DOMAIN, context={"source": SOURCE_IMPORT}, data=conf
                )
            except Exception as inst:
                _LOGGER.error(inst.args)
            _LOGGER.info("Tuya async setup flow_init")
            return result

        hass.async_create_task(flow_init())

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unloading the Tuya platforms."""
    _LOGGER.info("integration unload")
    unload = await hass.config_entries.async_unload_platforms(
        entry, hass.data[DOMAIN]["setup_platform"]
    )
    if unload:
        __device_manager = hass.data[DOMAIN][TUYA_DEVICE_MANAGER]
        __device_manager.mq.stop()
        __device_manager.remove_device_listener(hass.data[DOMAIN][TUYA_MQTT_LISTENER])

        hass.data.pop(DOMAIN)

    return unload


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Async setup hass config entry."""
    _LOGGER.info(f"tuya.__init__.async_setup_entry-->{entry.data}")

    hass.data[DOMAIN] = {TUYA_HA_TUYA_MAP: {}, TUYA_HA_DEVICES: []}
    hass.data[DOMAIN][TUYA_SETUP_PLATFORM] = set()

    success = await _init_tuya_sdk(hass, entry)
    if not success:
        return False

    return True
