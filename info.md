# Tuya Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

<p align="center">
    <img src="https://images.tuyacn.com/app/hass/ha_tuya.png" width="70%">
</p>

Home Assistant custom integration for controlling **Powered by Tuya (PBT)** devices using [Tuya Open API](https://developer.tuya.com/en/docs/cloud/?_source=github), officially maintained by the Tuya Developer Team.

## Supported Tuya Device Types

The following Tuya Device types are currently supported by this integration:

- [Light](https://github.com/tuya/tuya-home-assistant/blob/master/custom_components/tuya/light.py): Supports Tuya WiFi light devices
- [Switch](https://github.com/tuya/tuya-home-assistant/blob/master/custom_components/tuya/switch.py): Supports Tuya WiFi switch devices

Please check the [Develop Tuya-Compatible Home Assistant Drivers](https://developer.tuya.com/en/demo/devhomeassistantplugin/?_source=github) and [Home Assistant Entity](https://developers.home-assistant.io/docs/core/entity) tutorials to develop more drivers for the Tuya Home Assistant Integration and support more Tuya devices.

## Installation

### 1. Home Assistant Installation

Please refer to the [Home Assistant Offcial Installation](https://www.home-assistant.io/installation/) documentation to install **Home Assistant Core**.

You can also get help from [Set up Home Assistant Development Environment on Raspberry Pi](https://developer.tuya.com/en/demo/setuphomeassistantdevenv/?_source=github) in Tuya Developer Demo Center.

### 2. Tuya Home Assistant Integration Installation

There are two methods to install the integration:

1. Home Assistant Custom Components Installation
2. Install by [HACS](https://hacs.xyz/)

#### 2.1 Home Assistant Custom Components Installation

Download this tuya-home-assistant repo, unzip it, and copy the **custom_components/tuya/** folder to the HomeAssistant configuration directory, e.g. ~/.homeassistant

<img src="https://images.tuyacn.com/smart/hass/hass_integrations_1.png" height="300" />

#### 2.2 Install by HACS

**1.** [HACS Install](https://hacs.xyz/docs/installation/installation/)

**2.** [HACS Initial Configuration](https://hacs.xyz/docs/configuration/basic)

**3.** HACS -> Integrations -> ... -> Custom repositories 

<img src="https://images.tuyacn.com/app/hass/hacs_install_custom.png" width="90%" />

**4.** Input the tuya-home-assistant github https url: **https://github.com/tuya/tuya-home-assistant.git** and select **Integration** as the Category type,  then click **ADD**.

<img src="https://images.tuyacn.com/app/hass/custom_repos.png" width="70%" />

**5.** Click "INSTALL"

<img src="https://images.tuyacn.com/app/hass/hacs_tuya_install.png" width="90%" />

#### 2.3 Restart Home Assistant

Configuration -> Server Controls -> RESTART

#### 2.4 Activate the Tuya Integration

Configuration -> Integrations -> ADD INTEGRATION -> Tuya Integration

<img src="https://images.tuyacn.com/app/hass/hacs_tuya_setup.png" width="90%" />

### 3. Enter your Tuya credential

Please get the Tuya credential info by following the **Configure Cloud Development Project** part in [Tuya IoT Platform Configuration Guide](https://github.com/tuya/tuya-android-iot-app-sdk-sample/blob/activator_tool/Tuya_IoT_Platform_Configuration_Guide.md#tuya-device-manager-app-android).

<img src="https://images.tuyacn.com/app/hass/hacs_tuya_credential.png" height="300"/>

## Start Home Assistant

Go to the home assistant installation folder `~/hass` and use the following command to activate it and run the hass service:

~~~
➜  hass source bin/activate
(hass) ➜  hass hass
~~~

<img src="https://images.tuyacn.com/app/hass/command_line.png" width="80%"/>

For more information, please refer to the [Home Assistant Core](https://www.home-assistant.io/installation/) tutorial for the startup process and run **hass**.

## Link Tuya Devices to Home Assistant

Please download and use the [Tuya Device Manager App](https://github.com/tuya/tuya-android-iot-app-sdk-sample/releases/) to pair Tuya devices to the Home Assistant for controlling. 

<img src="https://images.tuyacn.com/app/Hanh/login.jpg" width="30%" />

You can check [Tuya Device Manager App (Android)](https://github.com/tuya/tuya-android-iot-app-sdk-sample/blob/activator_tool/Tuya_IoT_Platform_Configuration_Guide.md#tuya-device-manager-app-android) part of the the Tuya IoT Platform Configuration Guide for more information.

## Issue feedback
You can give feedback on issues you encounter via **Github Issue**.