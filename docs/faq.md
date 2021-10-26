# FAQs

<font color=blue  size="4"><b>Q1: I got an error saying 'Config flow could not be loaded' when setting up the Tuya integration. How to fix it?</b></font>

<img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/16346315144df2e7c7a74.png" width="45%">

- You might have added Tuya v2 to Home Assistant. Tuya v2 is not compatible with the Tuya integration.

- Go to `custom_components` under the Home Assistant directory and delete the `tuya_v2` folder. Restart Home Assistant and try to install the integration again.

   <img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/16238163372b1ef921aab.png" width="40%" alt="Install Tuya Integration">

<font color=blue  size="4"><b>Q2: I got an error shown in the following screenshot when I tried to scan a QR code to link my devices to my cloud project. How to fix it?</b></font>

<img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/1634631751250784f4038.png" width="35%">

- This is because the data center you selected for your cloud project cannot serve the region of your app account. You must switch to the correct data center and scan the QR code again.

  1. Here is how to find the region: open the mobile app you use and tap **Me** > **Setting** > **Account and Security** > **Region**.

     <img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/16346317858db898f9179.png" width="35%">

  2. See [Mappings Between OEM App Accounts and Data Centers](https://developer.tuya.com/en/docs/iot/oem-app-data-center-distributed?id=Kafi0ku9l07qb) and find the data center that can serve your region.

  3. (Optional) If you do not find the data center you want to use, click the **Overview** tab and then **Edit** to add data centers.

     <img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/1634631515fc4ecfad158.png" width="80%">

  4. Click the **Devices** tab > **Link Tuya App Account**. Select the correct data center from the drop-down menu in the top right corner and click **Add App Account**.

     ![Image](https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/1634631514880ec6c4d6d.png)

  5. Scan the QR code again to link devices.

<font color=blue  size="4"><b>Q3: Will I be billed after the 1-year free trial of the API service expires?</b></font>

- After expiration, you can renew the subscription for free. The Trial Edition allows you to use all free API services but puts limits on the quota of API calls. For more information about the quota, see [Pricing](https://developer.tuya.com/en/docs/iot/membership-service?id=K9m8k45jwvg9j).

<font color=blue  size="4"><b>Q4: How to deal with the following errors?</b></font>

**Error code sample**:

```
[tuya-openapi] Response: {
  "code": 2406,
  "msg": "skill id invalid",
  "success": false,
  "t": 1624477851701
}
```

<br>

| Error code | Message | Troubleshooting |
|:----|:----|:----|
| 1004 | sign invalid | The Access ID and Access Secret you entered are not correct. For more information, see [Credentials Configuration](#config). |
| 1106 | permission deny | <ul><li> Your app account is not linked to your cloud project. This operation is a must-do. For more information, see [Link devices by app account](https://developer.tuya.com/en/docs/iot/Platform_Configuration_smarthome?id=Kamcgamwoevrx#title-3-Link%20devices%20by%20app%20account).</li><li> Incorrect account or password. You must enter the account and password of the mobile app that you use to scan the QR code for linking devices to your cloud project on the [Tuya IoT Development Platform](https://iot.tuya.com/).</li><li>Incorrect country. You must select the region of your account of the Tuya Smart app or Smart Life app.</li></ul> |
| 2406 | skill id invalid | Your cloud project on the [Tuya IoT Development Platform](https://iot.tuya.com) should be created after May 25, 2021. Otherwise, you need to create a new project. For more information, see [Operation on the Tuya IoT Development Platform](https://developer.tuya.com/en/docs/iot/migrate-from-an-older-version?id=Kamee9wtbd00b#title-3-Operation%20on%20the%20Tuya%20IoT%20Platform). |
| 28841105 | No permissions. This project is not authorized to call this API | Insufficient API permissions. You need to subscribe to the required [API services](https://developer.tuya.com/en/docs/iot/applying-for-api-group-permissions?id=Ka6vf012u6q76#title-2-Subscribe%20to%20API%20services) and [authorize](https://developer.tuya.com/en/docs/iot/applying-for-api-group-permissions?id=Ka6vf012u6q76#title-3-Authorize%20project%20to%20call%20APIs) your cloud project to use these API services. The following API services are required.<ul><li>Authorization</li><li>Device Connection Service</li><li>Smart Home Scene Linkage</li><li>IoT Data Analytics</li><li>Device Status Notification</li></ul> |