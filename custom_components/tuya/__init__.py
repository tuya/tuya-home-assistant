#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Support for Tuya Smart devices."""

import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, SOURCE_IMPORT
from homeassistant.core import HomeAssistant, Config
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

from typing import Any

from .const import (
    DOMAIN,
    CONF_ENDPOINT,
    CONF_ACCESS_ID,
    CONF_ACCESS_SECRET,
    CONF_USERNAME,
    CONF_PASSWORD,
    TUYA_TYPE_TO_HA
)

from .factory import crete_tuya_ha_device

from tuya_iot import (
    TuyaOpenAPI,
    TuyaOpenMQ,
    TuyaAssetManager,
    TuyaDeviceManager,
    TuyaDevice,
)

_LOGGER = logging.getLogger(__name__)


CONFIG_SCHEMA = vol.Schema(
    vol.All(
        cv.deprecated(DOMAIN),
        {
            DOMAIN: vol.Schema(
                {
                    vol.Required(CONF_ENDPOINT): cv.string,
                    vol.Required(CONF_ACCESS_ID): cv.string,
                    vol.Required(CONF_ACCESS_SECRET): cv.string,
                    vol.Required(CONF_USERNAME): cv.string,
                    vol.Required(CONF_PASSWORD): cv.string,
                }
            )
        },
    ),
    extra=vol.ALLOW_EXTRA,
)


def _init_tuya_sdk(hass: HomeAssistant, entry_data: dict) -> TuyaDeviceManager:
    api = TuyaOpenAPI(
        entry_data[CONF_ENDPOINT], entry_data[CONF_ACCESS_ID], entry_data[CONF_ACCESS_SECRET])
    api.set_dev_channel('hass')

    response = api.login(entry_data[CONF_USERNAME], entry_data[CONF_PASSWORD])
    if response.get('success', False) == False:
        _LOGGER.error(
            "Tuya login error response: %s",
            response,
        )
        return False

    mq = TuyaOpenMQ(api)
    mq.start()

    # Get device list
    devIds = []
    assetManager = TuyaAssetManager(api)
    response = assetManager.getAssetList()
    assets = response.get('result', {}).get('assets', [])
    for asset in assets:
        asset_id = asset['asset_id']
        devIds += assetManager.getDeviceList(asset_id)

    # Update device status
    deviceManager = TuyaDeviceManager(api, mq)
    deviceManager.updateDeviceCaches(devIds)

    # Create ha devices
    haDevices = []
    for (devId, device) in deviceManager.deviceMap.items():
        haDevice = crete_tuya_ha_device(device, deviceManager)
        if haDevice:
            haDevices.append(haDevice)

    hass.data[DOMAIN] = {
        'haDevices': haDevices,
    }

    # Set mqtt listener
    def _onMessage(msg):
        devId = msg.get('data', {}).get('devId', '')
        haDevices = hass.data[DOMAIN]['haDevices']
        for haDevice in haDevices:
            if haDevice.tuyaDevice.id == devId:
                haDevice.schedule_update_ha_state()

    mq.add_message_listener(_onMessage)

    return True


async def async_setup(hass, config):
    """Set up the Tuya integration."""

    conf = config.get(DOMAIN)
    print('Tuya async setup conf %s \n' % conf)
    if conf is not None:
        async def flow_init() -> Any:
            try:
                result = await hass.config_entries.flow.async_init(
                    DOMAIN, context={"source": SOURCE_IMPORT}, data=conf
                )
            except Exception as inst:
                print(inst.args)
            print("Tuya async setup flow_init")
            return result

        hass.async_create_task(
            flow_init()
        )

    # print("Tuya async setup true \n")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    print("tuya.__init__.async_setup_entry-->", entry.data)

    success = await hass.async_add_executor_job(_init_tuya_sdk, hass, entry.data)
    if not success:
        return False

    
    for platform in set(TUYA_TYPE_TO_HA.values()):
        print("tuya async platform-->", platform)
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(
                entry, platform
            )
        )

    return True
