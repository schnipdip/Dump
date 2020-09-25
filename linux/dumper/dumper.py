#!/usr/bin python3

#from watchdog.observers import Observeir
import configparser
import subprocess
import usb.core
import usb.util
import logger
import pyudev
import sys
import os
import re

def get_configParser():
    config = configparser.ConfigParser()
    config.read('../settings.ini')
    
    backup_device = config['settings']['backup_device_name']
    input_device = config['settings']['input_device_name']

    return backup_device, input_device


def find_backup():
    #Find all USB Devices
    connected_usb = usb.core.find(find_all=True)

    #Check if no devices are connected
    if connected_usb == None:
        raise ValueError('No Devices Found.')

    #Loop through connected devices and append to array
    device_list = []

    for device in connected_usb:
        usb_device = usb.util.get_string(device, device.iManufacturer)
        
        device_list.append(usb_device)

    return device_list
    
def verify_usb(usb_device_list, backup_device, input_device):
    for usb in usb_device_list:
        if backup_device in usb.lower():
            print('found the backup device')
            backup_usb_device = usb
        if input_device.lower() in usb.lower():
            print('found input device')
            input_usb_device = usb
    else:
        raise ValueError('The attached USB devices to not match the devices in ../settings.ini')

    return backup_usb_device, input_usb_device

if __name__ == "__main__":
    #get backupdevice and input device
    backup_device, input_device = get_configParser()
    
    #get connected usb devices
    usb_device = find_backup()
    
    #validate if backup and input devices are connected
    backup_usb_device, input_usb_device = verify_usb(usb_device, backup_device, input_device)

