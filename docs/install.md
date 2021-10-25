# Install Tuya Integration

[![En](https://img.shields.io/badge/Docs-English-orange)](https://github.com/tuya/tuya-home-assistant/wiki/Install-Tuya-v2?_source=d10de34623e3daca5b02e3c31528a0c4) [![Zh](https://img.shields.io/badge/Docs-中文-orange)](https://github.com/tuya/tuya-home-assistant/wiki/%E5%AE%89%E8%A3%85-Tuya-v2)

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

    <img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/16238163372b1ef921aab.png" width="30%" alt="Installation">

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

In **Configuration** > **Integrations** > **ADD INTEGRATION**, search for the keyword **tuya** and select **Tuya v2**.

<img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/162320853943fdfc9239d.png" width="50%" />

### 3. Enter your Tuya credential

In the Tuya Integration window, select **Smart Home PaaS** and click **SUBMIT**.

<img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/16256397792068fafbcc9.png" width="30%"/>

See the following table and enter your Tuya credential. 

| Field | Description |
| ------- | -------- |
| Access ID and Access Secret| Go to your cloud project on [Tuya IoT Platform](https://iot.tuya.com/cloud/?_source=3a6f90da0e85f686f89c4f85c883e8f0). Find the **Access ID** and **Access Secret** on the **Project Overview** tab.|
| Mobile App | Must select the one you used to link devices on the Tuya IoT Platform. |
| Country Code | The country you select on logging in to Tuya Smart or Smart Life app.  |
| Account | Tuya Smart or Smart Life app account. |
| Password | The password of your app account. |
> **Note**: The app mentioned in the table must be the one you used to link devices on the Tuya IoT Platform.
