# How to Developer a New Driver

For example, I want my socket called "Living Room Socket" to work in Tuya.

## I. Getting information about the device
First, get the logs according to [How to get logs](./get_log.md) and look up "living room socket" in the logs to get information about the device, such as
```json
{
      "active_time": 1623229189,
      "biz_type": 18,
      "category": "cz",
      "create_time": 1560491945,
      "icon": "smart/product_icon/cz.png",
      "id": "xxxxxxxxxxxxxxxx",
      "ip": "xxxxxxxxxxxxxxxx",
      "lat": "30.30286857361191",
      "local_key": "xxxxxxxxxxxxx",
      "lon": "120.0639743842656",
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
      "uid": "ay1622097934070h5Mpi",
      "update_time": 1625101929,
      "uuid": "65015854bcddc21a9073"
    }
```
## II. Finding category support
### 2.1 Tuya device category Instruction Set.
Get `"category": "cz"` from the log, I learn that my socket is in the category defined by Tuya as cz.
Go to the [Tuya developer website](https://developer.tuya.com/en/docs/iot/standarddescription?id=K9i5ql6waswzq&_source=523ce082061eb112a40973f8bbc6908b) to find the Instruction set corresponding to the cz category.

<img src="https://images.tuyacn.com/smart/hass/hass_driver_1.png" width="30%">

### 2.2 Home Assistant supports Entities
Based on my socket, I looked up the supported Entity models from the Home Assistant Entities, and here I found that the SwitchEntity was a better match for my socket device.
## III. Driver development
Based on the SwitchEntity selected in Home Assistant, I create a new switch.py file in tuya_v2.
### 3.1 Supported categories
Since we need to support cz, write in the switch.py file
```python
TUYA_SUPPORT_TYPE = {
    "cz", # Switch
}
```
In the TUYA_SUPPORT_HA_TYPE of const.py make sure the Home Assistant domain corresponding to SwitchEntity which is "switch" exists; if it doesn't, then add it in TUYA_SUPPORT_HA_TYPE.

```python
TUYA_SUPPORT_HA_TYPE = [
    "switch",   
    "fan",
    "cover",
    "climate",
    "light",
    "sensor",
    "binary_sensor",
    "humidifier",
    "number",
    "vacuum"
]
```
### 3.2 Device registration logic
```python
async def async_setup_entry(
    hass: HomeAssistant, _entry: ConfigEntry, async_add_entities
):
    """Set up tuya sensors dynamically through tuya discovery."""
    _LOGGER.info("switch init")

    hass.data[DOMAIN][TUYA_HA_TUYA_MAP].update({DEVICE_DOMAIN: TUYA_SUPPORT_TYPE})

    async def async_discover_device(dev_ids):
        """Discover and add a discovered tuya switch."""
        _LOGGER.info(f "switch add-> {dev_ids}")
        if not dev_ids:
            return
        entities = await hass.async_add_executor_job(_setup_entities, hass, dev_ids)
        hass.data[DOMAIN][TUYA_HA_DEVICES].extend(entities)
        async_add_entities(entities)

    async_dispatcher_connect(
        hass, TUYA_DISCOVERY_NEW.format(DEVICE_DOMAIN), async_discover_device
    )

    device_manager = hass.data[DOMAIN][TUYA_DEVICE_MANAGER]
    device_ids = []
    for (device_id, device) in device_manager.device_map.items():
        if device.category in TUYA_SUPPORT_TYPE:
            device_ids.append(device_id)
    await async_discover_device(device_ids)


def _setup_entities(hass, device_ids: list):
    """Set up Tuya Switch device."""
    device_manager = hass.data[DOMAIN][TUYA_DEVICE_MANAGER]
    entities = []
    for device_id in device_ids:
        device = device_manager.device_map[device_id]
        if device is None:
            continue

        for function in device.function:
            if function.startswith(DPCODE_SWITCH):
                entities.append(TuyaHaSwitch(device, device_manager, function))
                continue

    return entities
```
### 3.2 Properties
From the Entity documentation for Home Assistant Switch, you can see that the Properties parameter to be overridden is is_on.

<img src="https://images.tuyacn.com/smart/hass/hass_driver_2.png" width="50%">

It's used to indicate the on/off status of the socket. You can find that the corresponding Tuya category code of sockets is "cz", and the DP code to control the switch state in the instruction set is "switch". You can also find the code "switch" in the status section of the log. 
```json
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
      ]
```
It is known that the DP code "switch" exists in the status of this device, so
Define `DPCODE_SWITCH` as the switch DP code and rewrite the method is_on:
```python
    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self.tuya_device.status.get(self.dp_code, False)
```

### 3.3 Methods
The Methods that need to be rewritten can be viewed in the Entity documentation for Home Assistant Switch 

<img src="https://images.tuyacn.com/smart/hass/hass_driver_3.png" width="50%">

The "turn_on" and "turn_off" methods are used to turn on and turn off the socket. You can find its Tuya category code is "cz" and the DP code to control the switch state is "switch", and get the device set information of the device from the log.
```json
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
```
We know that there is a DP code "switch" in the functions of this device, so
reuse `DPCODE_SWITCH`, rewrite methods turn_on and turn_off

```python
def turn_on(self, **kwargs: Any) -> None:
    """Turn the switch on."""
    self._send_command([{"code": self.dp_code, "value": True}])

def turn_off(self, **kwargs: Any) -> None:
    """Turn the device off."""
    self._send_command([{"code": self.dp_code, "value": False}])
```
Now we have finished writing the socket driver.
### 3.4 Debugging
Debug by enabling the tuya_v2 log.
## IV. Reference code
https://github.com/tuya/tuya-home-assistant/blob/master/custom_components/tuya_v2/switch.py
## V. Reference documents
Tuya DP Code Data Type and Value Constraint: https://developer.tuya.com/en/docs/iot/datatypedescription?id=K9i5ql2jo7j1k&_source=751e806efb9d0a8cb3793945cccdc47e
