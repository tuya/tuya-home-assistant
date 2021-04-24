# tuya-official-homeassistant
[中文版](README_zh.md) | [English](README.md)

tuya-official-homeassistant是涂鸦官方维护的home assistant 插件。

## 支持设备类型
当前支持以下Home Assistant设备类型：
- Light: 支持主流涂鸦wifi灯设备
- Switch: 支持主要涂鸦wifi 开关设备

## Installation
### 1. Home Assistant 安装
参考[Home Assistant Installation](https://www.home-assistant.io/installation/) 文档进行安装 **Home Assistant Core**.
### 2. tuya-home-assistant 插件安装
tuya-home-assistant 支持两种方式进行安装
1. 通过Home Assistant Custom Components 方式进行安装
2. 通过[HACS](https://hacs.xyz/) 进行安装
#### 2.1 Home Assistant Custom Components 安装
从github上下载 tuya-home-assistant，解压缩，复制到HomeAssistant 设置目录, 如 **~/.homeassistant**

<img src="https://images.tuyacn.com/smart/hass/hass_integrations_1.png" height="300" />

#### 2.2 通过HACS安装
1. [HACS安装](https://hacs.xyz/docs/installation/installation/)
2. [HACS初始配置](https://hacs.xyz/docs/configuration/basic)
3. HACS -> Integrations -> ... -> Custom repositories 
<img src="./imgs/hacs_install_custom.png" height="250" />
4. 输入 tuya-home-assistant github https url 并在Category中选择Integration, 点击 "ADD"
<img src="./imgs/hacs_custom_repositories.png" height="150" />
5. 点击 "INSTALL"
<img src="./imgs/hacs_tuya_install.png" height="200"/>
#### 2.3 Restart Home Assistant
Configuration -> Server Controls -> RESTART
#### 2.4 Activate tuya-home-assistant
Configuration -> Integrations -> ADD INTEGRATION -> Tuya Integration
<img src="./imgs/hacs_tuya_set_up.png" height="200"/>

### 3. Enter your Tuya credential
<img src="./imgs/hacs_tuya_credential.png" height="300"/>


### tuya-official-homeassistant configuration
Refer to xxx to get the application information and configure it in the configuration.yaml in the configuration directory

<img src="https://images.tuyacn.com/smart/hass/hass_integrations_2.png" width="300" />

## 启动
参考**Home Assistant Core**教程中启动流程，运行
**hass**

## 开发插件、贡献代码
参考 [Contributing.md](./Contributing.md)

## 问题反馈
您可以通过**Github Issue** 或通过[**工单**](https://service.console.tuya.com)来进行反馈您所碰到的问题

## LICENSE
更多信息请参考[LICENSE](LICENSE)文件
