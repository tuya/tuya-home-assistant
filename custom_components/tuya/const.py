#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Constants for the Tuya integration."""

DOMAIN = "tuya"

CONF_ENDPOINT = "endpoint"
CONF_ACCESS_ID = "access_id"
CONF_ACCESS_SECRET = "access_secret"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

TUYA_ENDPOINT = {
    "https://openapi.tuyaus.com": "America",
    "https://openapi.tuyacn.com": "China",
    "https://openapi.tuyaeu.com": "Europe",
    "https://openapi.tuyain.com": "India",
    "https://openapi-ueaz.tuyaus.com": "EasternAmerica",
    "https://openapi-weaz.tuyaeu.com": "WesternEurope"
}

TUYA_TYPE_TO_HA = {
    "dj": "light",  # 灯具
    "kg": "switch",  # 开关
    "cz": "switch",  # 插座
    "pc": "switch",  # 排插
}
