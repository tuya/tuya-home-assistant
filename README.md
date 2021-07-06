# Tuya Home Assistant Integration

<p align="center">
    <img src="https://images.tuyacn.com/app/hass/ha_tuya.png" width="70%">
</p>

Tuya Home Assistant integration is developed for controlling **Powered by Tuya (PBT)** devices using [Tuya Open API](https://developer.tuya.com/en/docs/cloud/?_source=6c7c0e6d9fc9ac8296e1a48954e1d0e4), officially maintained by the Tuya Developer Team.

## [Tuya Beta Test Program](https://pages.tuya.com/develop/HomeAssistantBetaTest_V2?_source=df3c37ad796d2388fc5527a8029c7889)
Welcome to join the [Tuya Beta Test Program](https://pages.tuya.com/develop/HomeAssistantBetaTest_V2?_source=df3c37ad796d2388fc5527a8029c7889) to get your development gifts and make a contribution to the integration. Your feedback is valuable to the whole community.

## Supported Tuya Device Types
Five primary categories, 26 secondary categories are supported now!
[Supported Device Category](https://github.com/tuya/tuya-home-assistant/wiki/Supported-Device-Category)


 :tada: :tada: :tada: [Vote for Tuya v2 Integration New Device Driver Support!](https://github.com/tuya/tuya-home-assistant/discussions/86) :tada::tada::tada:


Please check the [Develop Tuya-Compatible Home Assistant Drivers](https://developer.tuya.com/en/demo/devhomeassistantplugin/?_source=edb3f773114ae82d9b55a9602a9b8e64) and [Home Assistant Entity](https://developers.home-assistant.io/docs/core/entity) tutorials to develop more drivers for the Tuya Home Assistant Integration and support more Tuya devices.

## Follow us
- <img src="https://img.icons8.com/color/48/000000/twitter--v1.png"/>  [Twitter](https://twitter.com/developwithtuya)
- <img src="https://img.icons8.com/material-two-tone/48/000000/youtube.png"/>  [YouTube](https://www.youtube.com/channel/UC25KgSG1nXMZmR8ehs3tleA)
- <img src="https://img.icons8.com/fluent/48/000000/facebook-new.png"/>  [Facebook](https://www.facebook.com/Develop-With-Tuya-104216298552203)
- <img src="https://images.tuyacn.com/smart/hass/hass_readme_brand_bilibili.png"/>  [Bilibili](https://space.bilibili.com/1394005610?from=search&seid=1788260158867313813)
- <img src="https://img.icons8.com/fluent/48/000000/linkedin.png"/>  [Linkedin](https://www.linkedin.com/company/develop-with-tuya)

Follow us to get more information and leading technology on the Internet of Things, as well as updates and activities on the [Tuya IoT Developer Platform](https://developer.tuya.com/)

## Workflow

<img src="https://images.tuyacn.com/app/hass/hass_diagram1.png" width="60%"/> <img src="https://images.tuyacn.com/app/hass/workflow.png" width="35%" />

## Sequence Diagram

<img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/16194063817c985ee4c2f.png" width="60%" />

## Tuya Home Assistant Integration User Guide

For more information, please check [How to Use Tuya Home Assistant Integration](https://developer.tuya.com/en/docs/iot/Home_Assistant_Integration?id=Kamcjcbvk2mu8&_source=1f6c7c604f6cc5057a3befbe1092b263).

Youtube tutorial:

[![Youtube](https://img.youtube.com/vi/Amc_fmYMQEo/0.jpg)](https://www.youtube.com/watch?v=Amc_fmYMQEo)

## Installation

### 1. Home Assistant Installation

Please refer to the [Home Assistant Official Installation](https://www.home-assistant.io/installation/) documentation to install **Home Assistant Core**.

You can also get help from [Set up Home Assistant Development Environment on Raspberry Pi](https://developer.tuya.com/en/demo/setuphomeassistantdevenv/?_source=b1441bb02314be3e594a0448891aac58) in Tuya Developer Demo Center.

### 2. Tuya Home Assistant Integration Installation

>**Note**：The new version of Tuya Home Assistant integration (Tuya v2) can be compatible with the old version. Both versions can be installed at the same time. You don’t need to uninstall the old version before installing the new version.

There are two methods to install the integration:

* Home Assistant Custom Components Installation
* Install by [HACS](https://hacs.xyz/)

#### 2.1 Home Assistant Custom Components Installation

1. Download the [tuya-home-assistant repo](https://github.com/tuya/tuya-home-assistant?_source=a8502ebc9cd2966eaef661d1945d4284).
2. Unzip it and copy the `custom_components/tuya/` folder to the Home Assistant configuration directory, for example, `~/.homeassistant`.

    <img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/16238163372b1ef921aab.png" width="40%" alt="Installation">

#### 2.2 Install by HACS

1. See [HACS Official Installation Guide](https://hacs.xyz/docs/installation/installation/) and install HACS.

2. See [Initial Configuration Guide](https://hacs.xyz/docs/configuration/basic) and complete initial configuration.

3. Open Home Assistant. Click **HACS** > **Integrations** > **⋮** > **Custom repositories**.
    <img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/16221073906e836eba5eb.png" width="90%" />

4. Enter `https://github.com/tuya/tuya-home-assistant` in the address bar at the bottom left of the window. Select **Integration** from the **Category** list and click **ADD**.

    <img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/162384530830e42682b3c.png" width="70%" />

5. In the dialog box that appears, click **INSTALL**.

    <img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/16238453803774d728b74.png" width="70%" />

#### 2.3 Restart Home Assistant

You can restart the Home Assistant server in **Configuration** > **Server Controls** > **RESTART**.
    <img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/16242415480daab38307a.png" width="70%" />


#### 2.4 Set up the Tuya Integration

In **Configuration** > **Integrations** > **ADD INTEGRATION** > **Tuya Integration**, search for the keyword **tuya** and select **Tuya v2**.

<img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/162320853943fdfc9239d.png" width="70%" />

### 3. Enter your Tuya credential

##### 3.1 Smart Home PaaS Development Type

In the Tuya Integration window, select **Smart Home PaaS** and click **SUBMIT**.
<img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/16242422923267ec834da.png" width="40%"/>

See the following table and enter your Tuya credential. 

| Field | Description |
| ------- | -------- |
| Access ID and Access Secret| Go to your cloud project on [Tuya IoT Platform](https://iot.tuya.com/cloud/?_source=3a6f90da0e85f686f89c4f85c883e8f0). Find the **Access ID** and **Access Secret** on the **Project Overview** tab.|
| Mobile App | Must select the one you used to link devices on the Tuya IoT Platform. |
| Country Code | The country you select on logging in to Tuya Smart or Smart Life app.  |
| Account | Tuya Smart or Smart Life app account. |
| Password | The password of your app account. |

> **Note**: The app mentioned in the table must be the one you used to link devices on the Tuya IoT Platform.
##### 3.2 Custom Development Type

From the Tuya Integration window, select **Custom Development** and click **SUBMIT**.

See the table in 3.1 and enter your Tuya credential. 

<img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/16242426585f50a85bef9.png"  width="40%"/>

## Start Home Assistant

Go to the home assistant installation folder `~/hass` and use the following command to activate it and run the hass service:

```
➜  hass source bin/activate
(hass) ➜  hass hass
```

<img src="https://images.tuyacn.com/app/hass/command_line.png" width="80%"/>

For more information, please refer to the [Home Assistant Core](https://www.home-assistant.io/installation/) tutorial for the startup process and run **hass**.

## Link Tuya Devices to Home Assistant

Please download and use the Tuya Smart or Tuya Smart Life apps to pair Tuya devices to the Home Assistant for controlling. You can check the following links to download the apps.

- Tuya Smart App: [iOS App](https://apps.apple.com/us/app/tuyasmart/id1034649547) | [Android App](https://play.google.com/store/apps/details?id=com.tuya.smart&hl=en_US&gl=US)
- Tuya Smart Life App: [iOS App](https://apps.apple.com/us/app/smart-life-smart-living/id1115101477) | [Android App](https://play.google.com/store/apps/details?id=com.tuya.smartlife&hl=en_US&gl=US)

For more information, please check [How to Use Tuya Home Assistant Integration](https://developer.tuya.com/en/docs/iot/Home_Assistant_Integration?id=Kamcjcbvk2mu8&_source=1f6c7c604f6cc5057a3befbe1092b263).

## Contributing

Please refer to the [Contributing.md](./contributing.md) for contributing guide.

## Issue feedback

You can give feedback on issues you encounter via **GitHub Issue**.

## LICENSE

For more information, please refer to the [LICENSE](LICENSE) file.
