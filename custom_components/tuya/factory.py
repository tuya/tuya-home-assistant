#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from .light import TuyaHaLight
from .switch import TuyaHaSwitch

from .const import (
    TUYA_TYPE_TO_HA,
)

from tuya_iot import TuyaDevice, TuyaDeviceManager

def crete_tuya_ha_device(device: TuyaDevice, deviceManager: TuyaDeviceManager):
    haPlatform = TUYA_TYPE_TO_HA.get(device.category, '')
    if haPlatform == 'light':
        return TuyaHaLight(device, deviceManager)
    elif haPlatform == 'switch':
        return TuyaHaSwitch(device, deviceManager)
    else:
        return None
