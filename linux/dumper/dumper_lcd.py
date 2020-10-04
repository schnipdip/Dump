#!/usr/bin python3

import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import configparser
import subprocess
import logger
import pyudev
import time
import board
import busio
import usb
import sys
import os
import re

# 1. User plugs in USB -> USB Devices need to be validated
# 2. User selects USB Data source, other device is the backup device
# 3. Get USB Information:(idProduct, idManufacturer) for both devices
# 4. Mount USB's to /mnt/source and /mnt/backup
# 5. Present user with message backup is occuring, do not unplug devices
# 6. Perform RSYNC Backup
# 7. Once backup is completed, unmount disks
# 8. Present user with message it's safe to remove drives


def init_lcd():
    '''
        Params: lcd_columns - number of culumns the LCD Screen has
                lcd_rows    - number of rwos the LCD Screen has
                i2c         - calling i2c program
                lcd         - setting lcd screen
        return: lcd 

    '''
    
    lcd_columns = 16
    lcd_rows = 2
    i2c = busio.I2C(board.SCL, board.SDA)
    lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

    return lcd


def get_configparser():
    config = configparser.ConfigParser()
    config.read('/home/pi/dump/linux/settings.ini')

    backup_device = config['settings']['backup_device_name']
    input_device = config['settings']['input_device_name']
    dev_backup_loc = config['settings']['dev_backup_loc']
    dev_input_loc = config['settings']['dev_input_loc']
    mnt_backup_loc = config['settings']['mnt_backup_loc']
    mnt_input_loc = config['settings']['mnt_input_loc']
    dumper_loc = config['settings']['dumper_loc']

    return backup_device, input_device, dev_backup_loc, dev_input_loc, mnt_backup_loc, mnt_input_loc, dumper_loc

def check_usb():
    #LCD MESSAGE
    lcd.clear()
    lcd.message = "Detecting USBs"
    time.sleep(0.5)

    #Find all USB Devices
    connected_usb = usb.core.find(find_all=True)

    #Check if no devices are connected
    if connected_usb == None:
        lcd.clear()
        lcd.message = "No devices found"
        raise ValueError('No Devices Found.')

    #Loop through connected devices and append to array
    device_list = {}

    for device in connected_usb:
        usb_device = usb.util.get_string(device, device.iManufacturer)
        usb_device = str(usb_device)
        usb_device_vendorID = hex(device.idVendor)
        usb_device_productID = hex(device.idProduct)
        device_list[usb_device] = usb_device_vendorID, usb_device_productID
    
    lcd.clear()
    lcd.message = "Devices found"
    time.sleep(0.5)

    return device_list

def verify_usb(usb_device_list, backup_device, input_device):
    backup_device = backup_device.lower()
    input_device = input_device.lower()
    
    lcd.clear()
    lcd.message = "Validating USB"
    time.sleep(0.5)

    usb_list = {}
    for device, value in usb_device_list.items():
        print(usb_device_list[device][1])
        if backup_device in device.lower():
            print('found the backup device')
            backup_usb_device_vendor = usb_device_list[device][0]
            backup_usb_device_product = usb_device_list[device][1]
            #usb_list[device] = backup_usb_device_product

        if input_device in device.lower():
            print('found the input device')
            input_usb_device_vendor = usb_device_list[device][0]
            input_usb_device_product = usb_device_list[device][1]

    return backup_usb_device_vendor, input_usb_device_vendor, backup_usb_device_product, input_usb_device_product


def mount_usb(dbl, dil, mbl, mil, backup_name, input_name):
    check_path_backup = (mbl + 'backup')
    check_path_input = (mil + 'source')
    
    lcd.clear()
    lcd.message = "Mounting Devices"
    time.sleep(0.5)

    if os.path.exists(check_path_backup):
        pass
    else:
        #make dir for mount point
        makedir_backup = ('mkdir ' + mbl + 'backup')
        os.system(makedir_backup)

    if os.path.exists(check_path_backup):
        #make mount point for backup usb
        backup_command = ('sudo mount -t auto ' + dbl + ' ' + mbl + 'backup')
        os.system(backup_command)

        lcd.clear()
        lcd.message = "Backup Mounted"
        time.sleep(0.5)

    if os.path.exists(check_path_input):
        pass
    else:
        #make dir for mount point
        makedir_input = ('mkdir ' + mil + 'source')
        os.system(makedir_input)

    if os.path.exists(check_path_input):
        #make mount point for input usb
        input_command = ('sudo mount -t auto ' + dil + ' ' + mil + 'source')
        os.system(input_command)
        
        lcd.clear()
        lcd.message = "Source Mounted"
        time.sleep(0.5)
    

def run_autobackup(dev_backup_loc, dev_input_loc, mnt_backup_loc, mnt_input_loc, backup_name, input_name):
    lcd.clear()
    lcd.message = "Backing up data"
    time.sleep(0.5)

    lcd.clear()
    lcd.message = "Do NOT unplug\ndevices"

    INPUT_SOURCE = (mnt_input_loc + 'source')
    INPUT_DEVICE = (dev_input_loc)
    BACKUP_SOURCE = (mnt_backup_loc + 'backup')
    BACKUP_DEVICE = (dev_backup_loc)

    command = ('''rsync -a {0} {1} ''').format(INPUT_SOURCE, BACKUP_SOURCE)

    result = subprocess.run(command, shell=True)

    print (result)

def unmount_drives():
    lcd.clear()
    lcd.message = "Unmounting USBs"
    time.sleep(0.5)
    
    #unmount drives
    unmount_command = ('''umount /mnt/*''')
    subprocess.run(unmount_command, shell=True)
    
    #clean up /mnt/* paths
    cleanup_command = ('''rm -r /mnt/*''')
    subprocess.run(cleanup_command, shell=True)

    lcd.clear()
    lcd.message = "Safe to \nremove USBs"
    time.sleep(5)

if __name__ == "__main__":
    #init lcid screen
    lcd = init_lcd()

    #get configparser
    backup_device, input_device, dev_backup_loc, dev_input_loc, mnt_backup_loc, mnt_input_loc, dumper_loc = get_configparser()

    #message user to plug in devices
    # TODO: get message to scroll to the left without newline continuously
    while True:
        lcd.message = "Insert USB's\nPress Select"
    
        device_add = True
        while device_add == True:
            #perform USB check
            if lcd.select_button:
                print('select')
                #get connected usb devices
                usb_device = check_usb()

                #validate if backup and input devices are connected
                backup_usb_device_vendor, input_usb_device_vendor, backup_usb_device_product, input_usb_device_product = verify_usb(usb_device, backup_device, input_device)
            
                #mount USB
                mount_usb(dev_backup_loc, dev_input_loc, mnt_backup_loc, mnt_input_loc, backup_device, input_device)
            
                lcd.clear()
                lcd.message = "Press RB to\nbeing backup"
                #device_add = False
        
            if lcd.right_button:
                #check if /mnt/backup and /mnt/source exist
                verify_backup_loc = mnt_backup_loc + 'backup'
                verify_source_loc = mnt_input_loc + 'source'
            
                print(verify_backup_loc)
                print(verify_source_loc)

                if os.path.exists(verify_backup_loc) and os.path.exists(verify_source_loc):
                    #rsync backup -> right_button
                    run_autobackup(dev_backup_loc, dev_input_loc, mnt_backup_loc, mnt_input_loc, backup_device, input_device)

                    #unmount devices
                    unmount_drives()

                    device_add = False
                else:
                    lcd.clear()
                    lcd.message = "Press Select to\nMount USBs"
                    time.sleep(0.5)
            
            
