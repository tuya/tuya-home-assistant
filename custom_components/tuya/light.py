#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Support for the Tuya lights."""

import logging
import json
from typing import Any, Dict, List, Optional, Tuple, cast

from homeassistant.core import HomeAssistant, Config
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP,
    ATTR_HS_COLOR,
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR,
    SUPPORT_COLOR_TEMP,
    LightEntity,
)
from homeassistant.util import color as colorutil

from .const import (
    DOMAIN,
)

from .base import TuyaHaDevice

from tuya_iot import TuyaDeviceManager, TuyaDevice

_LOGGER = logging.getLogger(__name__)


# Light(dj)
# https://developer.tuya.com/docs/iot/open-api/standard-function/lighting/categorydj?categoryId=553018
DPCODE_SWITCH = 'switch_led'
DPCODE_WORK_MODE = 'work_mode'
DPCODE_BRIGHT_VALUE = 'bright_value'
DPCODE_TEMP_VALUE = 'temp_value'
DPCODE_COLOUR_DATA = 'colour_data'

MIREDS_MAX = 500
MIREDS_MIN = 153

HSV_HA_HUE_MIN = 0
HSV_HA_HUE_MAX = 360
HSV_HA_SATURATION_MIN = 0
HSV_HA_SATURATION_MAX = 100

WORK_MODE_WHITE = 'white'
WORK_MODE_COLOUR = 'colour'


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    print('tuya.light.async_setup_entry')

    haDevices = []
    for haDevice in hass.data[DOMAIN]['haDevices']:
        if haDevice.platform == 'light':
            haDevices.append(haDevice)
    
    
    async_add_entities(haDevices)

class TuyaHaLight(TuyaHaDevice, LightEntity):
    """Tuya light device."""

    platform = 'light'

    # ToggleEntity

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        return self.tuyaDevice.status.get(DPCODE_SWITCH, False)

    def turn_on(self, **kwargs: Any) -> None:
        """Turn on or control the light."""
        commands = []
        print("light kwargs->", kwargs)
        if (
            ATTR_BRIGHTNESS not in kwargs
            and ATTR_HS_COLOR not in kwargs
            and ATTR_COLOR_TEMP not in kwargs
        ):
            commands += [{'code': DPCODE_SWITCH, 'value': True}]

        if ATTR_BRIGHTNESS in kwargs:
            if WORK_MODE_COLOUR == self._work_mode():
                colour_data = self._get_hsv()
                v_range = self._tuya_hsv_v_range()
                # hsv_v = colour_data.get('v', 0)
                colour_data['v'] = self.remap(kwargs[ATTR_BRIGHTNESS], 0, 255, v_range[0], v_range[1])
                commands += [{'code': DPCODE_COLOUR_DATA, 'value': json.dumps(colour_data)}]
            else:
                new_range = self._tuya_brightness_range()
                tuya_brightness = int(self.remap(kwargs[ATTR_BRIGHTNESS], 0, 255, new_range[0], new_range[1]))
                commands += [{'code': DPCODE_BRIGHT_VALUE, 'value': tuya_brightness}]
                # commands += [{'code': DPCODE_WORK_MODE, 'value': self._work_mode()}]

        if ATTR_HS_COLOR in kwargs:
            colour_data = self._get_hsv()
            # hsv h
            colour_data['h'] = kwargs[ATTR_HS_COLOR][0]
            # hsv s
            ha_s = kwargs[ATTR_HS_COLOR][1]
            s_range = self._tuya_hsv_s_range()
            colour_data['s'] = self.remap(ha_s, HSV_HA_SATURATION_MIN, HSV_HA_SATURATION_MAX, s_range[0], s_range[1])
            # hsv v
            ha_v = self.brightness
            v_range = self._tuya_hsv_v_range()
            colour_data['v'] = self.remap(ha_v, 0, 255, v_range[0], v_range[1])

            commands += [{'code': DPCODE_COLOUR_DATA, 'value': json.dumps(colour_data)}]
            if self.tuyaDevice.status[DPCODE_WORK_MODE] != 'colour':
                commands += [{'code': DPCODE_WORK_MODE, 'value': 'colour'}]

        if ATTR_COLOR_TEMP in kwargs:
            # temp color
            new_range = self._tuya_temp_range()
            color_temp = self.remap(self.max_mireds - kwargs[ATTR_COLOR_TEMP] + self.min_mireds, self.min_mireds, self.max_mireds, new_range[0], new_range[1])
            commands += [{'code': DPCODE_TEMP_VALUE, 'value': int(color_temp)}]

            # brightness
            ha_brightness = self.brightness
            new_range = self._tuya_brightness_range()
            tuya_brightness = self.remap(ha_brightness, 0, 255, new_range[0], new_range[1])
            commands += [{'code': DPCODE_BRIGHT_VALUE, 'value': int(tuya_brightness)}]

            if self.tuyaDevice.status[DPCODE_WORK_MODE] != 'white':
                commands += [{'code': DPCODE_WORK_MODE, 'value': 'white'}]

        self.tuyaDeviceManager.sendCommands(self.tuyaDevice.id, commands)

    def turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        commands = [{'code': DPCODE_SWITCH, 'value': False}]
        self.tuyaDeviceManager.sendCommands(self.tuyaDevice.id, commands)

    # LightEntity

    @property
    def brightness(self):
        """Return the brightness of the light."""
        old_range = self._tuya_brightness_range()
        brightness = self.tuyaDevice.status.get(DPCODE_BRIGHT_VALUE, 0)

        if WORK_MODE_COLOUR == self._work_mode():
            colour_data = json.loads(self.tuyaDevice.status.get(DPCODE_COLOUR_DATA, 0))
            v_range = self._tuya_hsv_v_range()
            hsv_v = colour_data.get('v', 0)
            return int(self.remap(hsv_v, v_range[0], v_range[1], 0, 255))
        else:
            return int(self.remap(brightness, old_range[0], old_range[1], 0, 255))

        # return self.tuyaDevice.status.get(DPCODE_BRIGHT_VALUE, 0)

    def _tuya_brightness_range(self) -> (int, int):
        bright_value = json.loads(self.tuyaDevice.function.get(DPCODE_BRIGHT_VALUE, {}).values)
        return bright_value.get('min', 0), bright_value.get('max', 255)

    @property
    def hs_color(self):
        """Return the hs_color of the light."""
        colour_data = json.loads(self.tuyaDevice.status.get(DPCODE_COLOUR_DATA, 0))
        s_range = self._tuya_hsv_s_range()
        return colour_data.get('h', 0), self.remap(colour_data.get('s', 0), s_range[0], s_range[1], HSV_HA_SATURATION_MIN, HSV_HA_SATURATION_MAX)

    @property
    def color_temp(self):
        """Return the color_temp of the light."""
        new_range = self._tuya_temp_range()
        tuya_color_temp = self.tuyaDevice.status.get(DPCODE_TEMP_VALUE, 0)
        ha_color_temp = self.max_mireds - self.remap(tuya_color_temp, new_range[0], new_range[1], self.min_mireds, self.max_mireds) + self.min_mireds
        return ha_color_temp

    @property
    def min_mireds(self):
        """Return color temperature min mireds."""
        return MIREDS_MIN

    @property
    def max_mireds(self):
        """Return color temperature max mireds."""
        return MIREDS_MAX

    def _tuya_temp_range(self) -> (int, int):
        temp_value = json.loads(self.tuyaDevice.function.get(DPCODE_TEMP_VALUE, {}).values)
        return temp_value.get('min', 0), temp_value.get('max', 255)

    def _tuya_hsv_s_range(self) -> (int, int):
        colour_data = json.loads(self.tuyaDevice.function.get(DPCODE_COLOUR_DATA, {}).values)
        s = colour_data.get('s')
        return s.get('min', 0), s.get('max', 255)
    
    def _tuya_hsv_v_range(self) -> (int, int):
        colour_data = json.loads(self.tuyaDevice.function.get(DPCODE_COLOUR_DATA, {}).values)
        v = colour_data.get('v')
        return v.get('min', 0), v.get('max', 255)

    def _work_mode(self) -> str:
        return self.tuyaDevice.status.get(DPCODE_WORK_MODE, "")

    def _get_hsv(self) -> Dict[str, int]:
        return json.loads(self.tuyaDevice.status[DPCODE_COLOUR_DATA])

    @property
    def supported_features(self):
        """Flag supported features."""
        supports = 0
        if DPCODE_BRIGHT_VALUE in self.tuyaDevice.status:
            supports = supports | SUPPORT_BRIGHTNESS
        if DPCODE_COLOUR_DATA in self.tuyaDevice.status:
            supports = supports | SUPPORT_COLOR
        if DPCODE_TEMP_VALUE in self.tuyaDevice.status:
            supports = supports | SUPPORT_COLOR_TEMP
        return supports
