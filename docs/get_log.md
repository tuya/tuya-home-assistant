# How to Get the Log

[![En](https://img.shields.io/badge/Docs-English-orange)](https://github.com/tuya/tuya-home-assistant/wiki/How-to-Get-the-Log) [![Zh](https://img.shields.io/badge/Docs-中文-orange)](https://github.com/tuya/tuya-home-assistant/wiki/%E5%A6%82%E4%BD%95%E8%8E%B7%E5%8F%96%E6%97%A5%E5%BF%97)

With Home Assistant **logger** integration, we can get tuya integration's log which can help us fix bugs and develop new device drivers.

Add the following to your **configuration.yaml** file:
```python
logger:
  default: critical
  logs:
    custom_components.tuya_v2: debug
```
Then you can get the log from **home-assistant.log** 

<img src="https://images.tuyacn.com/smart/hass/hass_integrations_log_file.png" width="30%"/>

or **Configuration/Logs** with "LOAD FULL HOME ASSISTANT LOG"

<img src="https://images.tuyacn.com/smart/hass/hass_integrations_log_full.png" width="60%"/>

