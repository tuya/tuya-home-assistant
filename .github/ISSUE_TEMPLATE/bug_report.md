---
name: Bug report
about: Create a report to help us improve, Not leave sensitive info in the log.
title: ''
labels: bug
assignees: ''

---

**Describe the bug**

A clear and concise description of what the bug is.

**Expected behavior**

A clear and concise description of what you expected to happen.

**Diagnostics for integrations and devices**

You can download the diagnostics text file by clicking the "Download diagnostics" button in (Configuration -> Integrations -> Tuya Integration -> lower right button), please check the image below:

<img src="https://user-images.githubusercontent.com/907831/152950135-320e9ea2-45bc-4d80-b961-0db8eb9c7ae5.png" alt="image" width="250"/>

**Screenshots**

If applicable, add screenshots to help explain your problem.

**Home Assistant Version**
- e.g. 2021.5.1

**Device info (please complete the following information, which can be found in [log](https://github.com/tuya/tuya-home-assistant/wiki/How-to-get-the-log)):**

like this:
{
      "active_time": 1623229189,
      "biz_type": 18,
      "category": "cz",
      "create_time": 1560491945,
      "icon": "smart/product_icon/cz.png",
      "id": "aaaaaaaaaaa",
      "ip": "xxxxxxxxxxxxxxxx",
      "lat": "xxxxxxxxxx",
      "local_key": "xxxxxxxxxxxxx",
      "lon": "xxxxxxx",
      "model": "",
      "name": "Living Room Socket",
      "online": false,
      "owner_id": "34794909",
      "product_id": "yfemiswbgjhddhcf",
      "product_name": "Switch Product",
      "status": [
        {
          "code": "switch",
          "value": false
        },
        {
          "code": "countdown_1",
          "value": 0
        },
        {
          "code": "cur_current",
          "value": 0
        },
        {
          "code": "cur_power",
          "value": 0
        },
        {
          "code": "cur_voltage",
          "value": 2343
        }
      ],
      "sub": false,
      "time_zone": "+08:00",
      "uid": "xxxxxxxxxxxxxxxxxxx",
      "update_time": 1625101929,
      "uuid": "xxxxxxxxxxxxxxxxxx"
    }

**Device specifications (please complete the following information, which can be found in [log](https://github.com/tuya/tuya-home-assistant/wiki/How-to-get-the-log)):**

Same device's id, like this:
[2021-07-01 10:18:01,351] [tuya-openapi] Request: method = GET, url = https://openapi.tuyacn.com/v1.0/devices/aaaaaaaaaaa/specifications, params = None, body = None, headers = {'client_id': 'xxxxxxxxxxxx', 'sign': 'xxxxxxxxxxxx', 'sign_method': 'HMAC-SHA256', 'access_token': 'xxxxxxxxxxxxxxxx', 't': '1625105881351', 'lang': 'en'}
2021-07-01 10:18:01 DEBUG (SyncWorker_1) [tuya iot] Response: {
  "result": {
    "category": "cz",
    "functions": [
      {
        "code": "countdown_1",
        "type": "Integer",
        "values": "{\"unit\":\"s\",\"min\":0,\"max\":86400,\"scale\":0,\"step\":1}"
      },
      {
        "code": "switch",
        "type": "Boolean",
        "values": "{}"
      }
    ],
    "status": [
      {
        "code": "cur_voltage",
        "type": "Integer",
        "values": "{\"unit\":\"V\",\"min\":0,\"max\":2500,\"scale\":0,\"step\":1}"
      },
      {
        "code": "cur_current",
        "type": "Integer",
        "values": "{\"unit\":\"mA\",\"min\":0,\"max\":30000,\"scale\":0,\"step\":1}"
      },
      {
        "code": "switch",
        "type": "Boolean",
        "values": "{}"
      },
      {
        "code": "cur_power",
        "type": "Integer",
        "values": "{\"unit\":\"W\",\"min\":0,\"max\":50000,\"scale\":0,\"step\":1}"
      },
      {
        "code": "countdown_1",
        "type": "Integer",
        "values": "{\"unit\":\"s\",\"min\":0,\"max\":86400,\"scale\":0,\"step\":1}"
      }
    ]
  },
  "success": true,
  "t": 1625105881348
}

**Additional context**

Add any other context or logs about the problem here.
