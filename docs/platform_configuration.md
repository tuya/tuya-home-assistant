# Tuya IoT Platform Configuration Guide

[![En](https://img.shields.io/badge/Docs-English-orange)](https://github.com/tuya/tuya-home-assistant/wiki/Tuya-IoT-Platform-Configuration-Guide-Using-Smart-Home-PaaS?_source=27c468b2abbb019eb4983fc8cea49b90) [![Zh](https://img.shields.io/badge/Docs-中文-orange)](https://github.com/tuya/tuya-home-assistant/wiki/%E6%B6%82%E9%B8%A6-IoT-%E5%B9%B3%E5%8F%B0%E9%85%8D%E7%BD%AE%E6%8C%87%E5%8D%97%EF%BC%88%E5%85%A8%E5%B1%8B%E6%99%BA%E8%83%BD-PaaS-%E5%BC%80%E5%8F%91%E6%96%B9%E5%BC%8F%EF%BC%89)

This topic describes how to create a project on the [Tuya IoT Platform](https://iot.tuya.com/cloud/?_source=3a6f90da0e85f686f89c4f85c883e8f0), and connect to devices through the Tuya Smart app or the Smart Life app.

## Prerequisites

You have registered an account on the [**Tuya Smart** or **Smart Life**](https://developer.tuya.com/en/docs/iot/tuya-smart-app-smart-life-app-advantages?id=K989rqa49rluq#title-1-Download) app.

## Create a project

1. Log in to the [Tuya IoT Platform](https://iot.tuya.com/cloud/?_source=3a6f90da0e85f686f89c4f85c883e8f0).
2. In the left-side navigation bar, choose **Cloud**.
3. On the page that appears, click **Create Cloud Project**.
4. In the **Create Project** dialog box, set **Project Name**, **Description**, **Industry**, **Development Method**, and **Data Center**. From the **Development Method** drop-down list, select **Smart Home**.

   > **Note**: Open the **Tuya Smart** or **Smart Life** app. Tap **Me** and the **Setting** icon in the top right corner of the page, and find **Account and Security**. The **Region** field is what to be entered in **Data Center**. For more information about the data centers, see **Correspondence of regions and data centers**.

   <img src="https://images.tuyacn.com/app/hass/create_project.png" height="350pt"/>

5. Click **Create** to complete project creation.
6. On the **Authorize API Products** page, subscribe to the API product **Device status notification**.

   <img src="https://images.tuyacn.com/app/hass/device_notification.png" width="50%"/>

> **Note**: **Smart home** API products have been selected by default.

7. Click **Authorize**.

## Get authorization key

Click the newly created project to enter the **Project Overview** page and get the **Authorization Key** used to make API requests.

<img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/162208268849af51b8af3.png" height="300pt"/>

## Link devices by app account

Link the device by your app account and copy the **Device ID** on the **Device List** page as the value of `device_id`.

1. Go to the **Devices** page.
2. Choose **Link Tuya App Account** > **Add App Account**. ![image.png](https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/16272719727a6df1eb14f.png)
3. Scan the QR code with the **Tuya Smart** app or **Smart Life** app.

   <img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/16220137160a864a6099d.png" height="300pt"/>

4. Click **Confirm login** on the **Tuya Smart** app or **Smart Life** app.
5. Click the **All Devices** tab. You can see the devices linked with your **Tuya Smart** app or **Smart Life** app account.
