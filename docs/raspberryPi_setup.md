# Set up Home Assistant on a Raspberry Pi

[![En](https://img.shields.io/badge/Docs-English-orange)](https://github.com/tuya/tuya-home-assistant/wiki/Set-up-Home-Assistant-on-a-Raspberry-Pi) [![Zh](https://img.shields.io/badge/Docs-中文-orange)](https://github.com/tuya/tuya-home-assistant/wiki/%E5%9F%BA%E4%BA%8E%E6%A0%91%E8%8E%93%E6%B4%BE%E6%90%AD%E5%BB%BA-Home-Assistant-%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83)

This tutorial describes how to install Home Assistant Core on Raspberry Pi to get started with Home Assistant and set up the development environment.


Home Assistant is a Python-based open-source smart home system. It supports connection to smart devices across different platforms, which allows you to control a connected home with one system. 
We use Home Assistant Core (recommended for developers) to install Home Assistant OS and runs the program in Ubuntu Server. For more information about other installation methods, see the instructions on [Home Assistant](https://www.home-assistant.io/installation/).

## Preparation

### Prerequisites

You have installed Python on your system. Python 3.8.0 or later is recommended.

### Prepare hardware and software

| Hardware/Software | Description |
|:----|:----|
| Computer | A computer |
| Device to run Home Assistant | Raspberry Pi 3 or later <br>This tutorial uses the 64-bit Raspberry Pi 4, with 8 GB RAM. |
| Environment | Ubuntu Server 20.04.2 LTS |
| Wireless router | One piece |
| microSD card | One piece |
| SD Card reader | One piece |

## Steps
### Install the environment
1. Download and install [Raspberry Pi Imager 1.6](https://downloads.raspberrypi.org/imager/imager_1.6.dmg).

2. Insert the microSD card into your computer.

3. Start Raspberry Pi Imager 1.6 and click **CHOOSE OS**. 
<img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/goat/20210420/7810a2183da847eda2caa18e753bd73f.png" width="60%">

4. In the **Operating System** dialog box, select **Other general purpose OS** > **Ubuntu** > **Ubuntu Server 20.04.2 LTS (RPi 3/4/400)**. 
<img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/goat/20210420/44c57dbb581347cfb07c2fbeb39c5b5d.png" width="60%">

5. On the page of **Raspberry Pi Imager 1.6**, click **CHOOSE STORAGE** and select your microSD card. 
<img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/goat/20210420/44c57dbb581347cfb07c2fbeb39c5b5d.png" width="60%">

6. Click **WRITE** to flash the SD card with Raspberry Pi Imager. 
<img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/goat/20210420/a09e6d9990e4453c9841f2dbf4e1aba1.png" width="60%">

7. Waiting for flashing completed. 
<img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/goat/20210420/94bc74f72aea43afba78fcc6c6608e93.png" width="60%">

8. Remove the microSD card from your Mac and insert it into the Raspberry Pi.


### Connect Raspberry Pi to the internet
You can connect Raspberry Pi to the internet through a wired Ethernet connection (recommended) or a Wi-Fi network.
* Wired connection
Use an Ethernet cable to connect Raspberry Pi to the router.
* Wi-Fi connection
   1. Insert the flashed microSD card into your computer.
   2. Open **Finder** on your Mac and click **Locations** > **system-boot**.
   3. Open the **network-config** file with a text editor. Change the `myhomewifi` field to the SSID of your router and the `S3kr1t` field to the password of your router.
        ```
        wifis:
            wlan0:
                dhcp4: true
                optional: true
                access-points:
                myhomewifi:
                    password: "S3kr1t"
        ```
   4. Save the file and exit.
   5. Insert the microSD card into Raspberry Pi.

### Start Ubuntu Server
1. Find your Raspberry Pi's IP address on the local network from your router setup page. This tutorial uses `192.168.1.140` as an example.
2. Make sure your computer and Raspberry Pi connect to the same LAN. Execute the following command to connect to Raspberry Pi.
    ```
    ssh ubuntu@192.168.1.140
    ```
3. Enter the default password and then enter the new password twice to reset the password.
   > **Note**: The default username and password of Ubuntu Server both are `ubuntu`.

### Install Home Assistant
#### Install dependency

Execute the following three commands respectively to install dependencies. The installation process will take some time. 

```
sudo apt-get update
```

```
sudo apt-get upgrade -y
```

```
sudo apt-get install -y python3 python3-dev python3-venv python3-pip libffi-dev libssl-dev libjpeg-dev zlib1g-dev autoconf build-essential libopenjp2-7 libtiff5 --fix-missing
```


#### Create virtual environment

1. Create a directory for the installation of Home Assistant.
   
    ```
    mkdir ~/hass
    ```
2. Create and activate the virtual environment for Home Assistant.
   1. Go to the directory.
        ```
        cd ~/hass
        ```
   2. Create virtual environment.
        ```
        python3 -m venv .
        ```
   3. Activate virtual environment.
        ```
        source bin/activate
        ```
   
#### Install Home Assistant

1. Install Python package.
    ```
    python3 -m pip install wheel
    ```
2. Install Home Assistant Core.
    ```
    pip3 install homeassistant
    ```


#### Start Home Assistant
Execute the following command to start Home Assistant.
```
hass
```
When you start Home Assistant for the first time, the system will create `~/.homeassistant` directory to store configuration files and install required dependencies. This process will take some time.

Visit <http://192.168.1.140:8123> in a browser by using a device in the same LAN. If the Home Assistant homepage appears, it indicates that installation is successful.
> **Note**: The IP address here is only for demonstration. Use your Raspberry Pi's IP address.

<img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/goat/20210421/32d1b8de76f547b18b3bc5d9bafb2f8b.png" width="40%">

### Install Samba
We use Samba to share `.homeassistant` directory in the LAN. You can modify the `.homeassistant` file directly on your computer, which will help the development of drivers.

1. Install Samba.
    ```
    sudo apt-get install samba samba-common-bin
    ```
2. Configure `smb.conf` file.
   > **Note**: Yo must specify an absolute path to `smb.conf`, such as `/home/ubuntu/.homeassistant`.
   1. Edit the file.
        ```
        sudo vi /etc/samba/smb.conf
        ```
   2. Add the following line of code to the bottom of the configuration file.
        ```
        [pi]
        path = /home/ubuntu/.homeassistant
        writeable=Yes 
        create mask=0777 
        directory mask=0777 
        public=no 
        ```
   3. Save the file.
3. Add a Samba account.
   > **Note**: When you use the `sudo smbpasswd -a` command to create a Samba user, the account must be a Linux system account, such as ubuntu.
   1. Execute the following command line.
        ```
        sudo smbpasswd -a ubuntu
        ```
   2. Enter a password, such as `a123456`.
4. Restart Samba to make the configuration effective.
    ```
    sudo systemctl restart smbd
    ```
Once Samba is installed, the development environment is set up.

### Access Home Assistant folder through Samba

1. Open **Finder** on your Mac.
2. In the top-left corner of the screen, click **Go** > **Connect to Server**.
3. In the dialog box, enter your Raspberry Pi's IP address and click **Connect**.
    ```
    smb://192.168.1.140/pi
    ```
   > **Note**: The IP address here is only for demonstration. Use your Raspberry Pi's IP address.

   <img src="https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/1619166216a6f6b5c304d.png" width="60%">

4. In the dialog box, enter the account and password of the Samba user. See the following example.
   * Name: ubuntu
   * Password: a123456

5. Click **Connect** to access the Home Assistant folder shared with Raspberry Pi.

    ![Browse folder](https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/content-platform/hestia/16191665814cf607ed248.jpg)

## Summary
You can access the Home Assistant folder through Samba and proceed with the development of drivers. For more information, see [Develop Tuya-Compatible Home Assistant Drivers](https://developer.tuya.com/en/demo/devhomeassistantplugin?count=0.7387204857679788&_source=dc22d62a9924627fd8db9b750d54d93e).
