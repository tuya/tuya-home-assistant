---
name: New Device Support
about: New device that wants to be supported, Not leave sensitive info in the log.
title: ''
labels: enhancement, help wanted
assignees: ''

---

**Device normal info**
- Brand
- Model

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
      "lat": "xxxxxxxxxxxxxxxx",
      "local_key": "xxxxxxxxxxxxx",
      "lon": "xxxxxxxxxxxxxxx",
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
[2021-07-01 10:18:01,351] [tuya-openapi] Request: method = GET, url = https://openapi.tuyacn.com/v1.0/devices/aaaaaaaaaaa/specifications, params = None, body = None, headers = {'client_id': 'xxxxxxxxxxxx', 'sign': 'xxxxxxxxxxxx', 'sign_method': 'HMAC-SHA256', 'access_token': '213e2d4af5e8d217abc0b104462a9f72', 't': '1625105881351', 'lang': 'en'}
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
