[![Blue-dump-truck-svg.png](https://i.postimg.cc/9fzQ4LyN/Blue-dump-truck-svg.png)](https://postimg.cc/d7PYpmH8)

# Dump

Auto back up images from a raspberry pi to a removable storage device automatically from an SD card.

## Requirements
1. Raspberry Pi 4 B+  
2. Adafruit 16x2 with buttons --> [information](https://learn.adafruit.com/adafruit-16x2-character-lcd-plus-keypad-for-raspberry-pi)
3. SD Card Reader   --> found with [lsusb](https://linux.die.net/man/8/lsusb) -v
4. Removeable Hard Drive --> found with [lsusb](https://linux.die.net/man/8/lsusb) -v
5. The /dev/disk/by-id of Card Reader for FStab if it doesn't have a UUID
6. Python 3

## Get Started
1. Install the required python libraries `pip3 install -r requirements.txt`
2. Modify the settings in the `linux/settings.ini` file. --> *more information below*
3. Execute the installation script with `sudo`: `sudo sh install.sh lcd` or `sudo sh install.sh auto`. Use the `auto` installation if you aren't using an LCD screen to actively manage. Use `lcd` if you are using the 16x2 lcd screen.

## How to Use Dump with the LCD
In order to properly use Dump as it was intended, use the LCD screen. While not required, it allows you to actively manage and control your backups. It's safer. 

1. Connect your USB Devices into the two USB 3.0 ports for optimal performance. Make sure your USB devices operate at USB 3.0. This can be verified by using the `lsusb -v` command and observed by the `bcdUSB` descriptor.
2. Press the `select` button to start the backup. The backup source and the backup destination are determined in the `settings.ini` file.
3. Once everything is confirmed and mounted, select the `right` button to perform and `rsync` differential backup based on timestamps.
4. When the backup is completed and the dialog box that says it's safe to remove the drives appears, remove the drives. If you wish to run the backup again, simply hit the select button once you are returned back to the main screen `5 seconds` after the `It's safe to remove drives` dialog box appears. 
5. If you wish to `restart` the Raspberry Pi, simply hit the `up` button. This will restart the raspberry pi. A `3 second` timer will appear notifying you a restart is pending. 
6. If you wish to `shutdown` the Raspberry Pi, simply hit the `down` button. This will shutoff the raspberry pi. It's now safe to unplug the power supply from the Raspberry Pi.
7. For testing purposes, if the drives are already mounted and the mount directories exist, you can simply hit the `right` button to perform a differential backup. 

## Understanding the Settings.ini File

The settings file is comprised of a single `[settings]` field. Under this field there contains several variables that control how the devices are to be mounted and how to locate the devices. 

|Settings|  Information|
|--|--|
|dumper_loc| This for the `sh isntall.sh auto` setting. The location of dumper_no_lcd.py|
|backup_device_name| Generic name of the backup device. Can be found using `lsusb`. Can either add the full name or a portion of the known name. Example, `Sandisk`|
|input_device_name| Generic name of the source device. Can be found using `lsusb`. Can either add the full name or a portion of the known name. Example, `Lexar` |
| dev_backup_loc | The `/dev/` point for the backup device. Can be found using `lsblk` and some digging. Example, `/dev/disk/by-uuid/BA5C-B93C` |
| dev_input_loc | The `/dev/` point for the source device. Can be found using `lsblk` and some digging. Example, `/dev/disk/by-id/usb-Lexar_LRWM04U_201804030001-0\:0-part1` |
| mnt_backup_loc | The mount location of where the backup device from `/dev/` will be mounted to. Default is `/mnt/`. A folder will be created called `/mnt/backup` to mound the backup device to. |
| mnt_input_loc | The mount location of where the source device from `/dev/` will be mounted to. Default is `/mnt/`. A folder will be created called `/mnt/source` to mound the backup device to. |

## Troubleshooting

1. If you aren't pulling the git repo into `/home/pi/` then you need to open the `dumper_lcd.py` and/or `dumper_no_lcd.py` and change the source location for the `settings.ini` file. 
