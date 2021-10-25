# FAQs

[![En](https://img.shields.io/badge/Docs-English-orange)](https://github.com/tuya/tuya-home-assistant/wiki/FAQs) [![Zh](https://img.shields.io/badge/Docs-中文-orange)](https://github.com/tuya/tuya-home-assistant/wiki/%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E8%A7%A3%E7%AD%94)

**Q1. My devices have been paired with the Tuya Smart or Smart Life app in the old integration. Can they be seamlessly migrated to the new integration?**

Yes. All the pairing information is stored in the Tuya IoT Cloud. For the paired devices, you do not need to go through the pairing process again. However, you need to configure the automations in Home Assistant after migration.


**Q2. I get an error message saying **Invalid authentication**. How to fix this issue?**

<img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/1625307700fdcba246516.png" alt="image" style="zoom: 80%;" />


Please check the following things:

* Your cloud project on the [Tuya IoT Platform](https://iot.tuya.com/cloud/?_source=3a6f90da0e85f686f89c4f85c883e8f0) should be created after May 25, 2021. Otherwise, you need to create a new project or migrate data to a new project. For more information, see [Operation on the Tuya IoT Platform](https://developer.tuya.com/en/docs/iot/migrate-from-an-older-version?id=Kamee9wtbd00b&_source=25dc511869fe0d20fcf6b3ec25902277#title-3-Operation%20on%20the%20Tuya%20IoT%20Platform).
* On the [Tuya IoT Platform](https://iot.tuya.com/cloud/?_source=3a6f90da0e85f686f89c4f85c883e8f0), you have linked devices by using Tuya Smart or Smart Life app in your cloud project.
* You entered the correct account and password of the Tuya Smart or Smart Life app in the **Account** and **Password** fields. Note that the app account depends on which app (Tuya Smart or Smart Life) you used to link devices on the [Tuya IoT Platform](https://iot.tuya.com/cloud/?_source=3a6f90da0e85f686f89c4f85c883e8f0).


**Q3. Will I be billed after the 1-year free trial of the API product expires?**

After expiration, you can renew the subscription for free. The Trial Edition allows you to use all free API products but puts limits on the quota of API calls. For more information about the quota, see the [Pricing](https://developer.tuya.com/en/docs/iot/membership-service?id=K9m8k45jwvg9j&_source=3f0ae56a5ab2f91918cdc7b4fa60f2a0).

**Q4. I got the following error. How to fix it?**

```
[tuya-openapi] Response: {
  "code": 2406,
  "msg": "skill id invalid",
  "success": false,
  "t": 1624477851701
}
```

[![En](https://img.shields.io/badge/Docs-English-orange)](https://github.com/tuya/tuya-home-assistant/wiki/Error-code-and-Troubleshooting)[![Zh](https://img.shields.io/badge/Docs-中文-orange)](https://github.com/tuya/tuya-home-assistant/wiki/%E9%94%99%E8%AF%AF%E7%A0%81%E5%92%8C%E6%95%85%E9%9A%9C%E6%8E%92%E6%9F%A5#config)

[![En](https://img.shields.io/badge/Docs-English-orange)](https://github.com/tuya/tuya-home-assistant/wiki/Error-code-and-Troubleshooting)[![Zh](https://img.shields.io/badge/Docs-中文-orange)](https://github.com/tuya/tuya-home-assistant/wiki/%E9%94%99%E8%AF%AF%E7%A0%81%E5%92%8C%E6%95%85%E9%9A%9C%E6%8E%92%E6%9F%A5#config)

|Error Code|Error Message|Troubleshooting|
|:----|:----|:----|
|1004| sign invalid| Incorrect Access ID or Access Secret. Please refer to [Parameter Configuration](https://github.com/tuya/tuya-home-assistant/wiki/Install-Tuya-v2#3-enter-your-tuya-credential).
|1106|permission deny|<ul><li> App account not linked with cloud project: On the [Tuya IoT Platform](https://iot.tuya.com/cloud/?_source=3a6f90da0e85f686f89c4f85c883e8f0), you have linked devices by using Tuya Smart or Smart Life app in your cloud project. For more information, see [Link devices by app account](https://developer.tuya.com/en/docs/iot/Platform_Configuration_smarthome?id=Kamcgamwoevrx&_source=dc23ed1ea3e6988f278404eb2d403b1a#title-3-Link%20devices%20by%20app%20account).</li><li> Incorrect username or password: Enter the correct account and password of the Tuya Smart or Smart Life app in the **Account** and **Password** fields. Note that the app account depends on which app (Tuya Smart or Smart Life) you used to link devices on the [Tuya IoT Platform](https://iot.tuya.com/cloud/).</li><li>Incorrect availability zone: See [Availability Zone](https://github.com/tuya/tuya-home-assistant/wiki/Tuya-IoT-Platform-Configuration-Guide-Using-Smart-Home-PaaS#region--available-zone-correspondence) and select the correct availability zone.</li><li>Incorrect countycode: Fill the [code](https://countrycode.org/) of the country you select on logging in to Tuya Smart or Smart Life app.</li></ul>|
|1100|param is empty| Empty parameter of username or app. Fill the parameters refer to [Parameter Configuration](https://github.com/tuya/tuya-home-assistant/wiki/Install-Tuya-v2#3-enter-your-tuya-credential).
|2017|schema does not exist| Incorrect app selected. Select the app you used to link devices in the cloud project.| 
| 2406 | skill id invalid | Make sure that your cloud project on the [Tuya IoT Platform](https://iot.tuya.com/cloud/?_source=3a6f90da0e85f686f89c4f85c883e8f0) should be created after May 25, 2021. Otherwise, you need to create a new project or migrate data to a new project. For more information, see [Operation on the Tuya IoT Platform](https://developer.tuya.com/en/docs/iot/migrate-from-an-older-version?id=Kamee9wtbd00b&_source=25dc511869fe0d20fcf6b3ec25902277#title-3-Operation%20on%20the%20Tuya%20IoT%20Platform).|
| 28841105 |No permissions. This project is not authorized to call this API| Some APIs are not authorized, please  [Subscribe](https://developer.tuya.com/en/docs/iot/applying-for-api-group-permissions?id=Ka6vf012u6q76&_source=1d24d3bb945a53149684a949e1b11c9b#title-2-Subscribe%20to%20cloud%20products) then [Authorize](https://developer.tuya.com/en/docs/iot/applying-for-api-group-permissions?id=Ka6vf012u6q76&_source=dcf59d3fe3e69d95d2907cb636175080#title-3-Authorize%20projects%20to%20call%20the%20cloud%20product). The following APIs must be subscribed for this tutorial: <ul><li>Authorization</li><li>Smart Home Devices Management</li><li>Smart Home Family Management</li><li>Smart Home Scene Linkage</li><li>Smart Home Data Service</li><li>Device status notification</li></ul>|