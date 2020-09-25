#!/usr/bin python3

#from watchdog.observers import Observeir
import configparser
import subprocess
import usb
import logger
import pyudev
import sys
import os
import re
#import yaml

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
    device_list = {}

    for device in connected_usb:
        #print (device)
        usb_device = usb.util.get_string(device, device.iManufacturer)
        usb_device_vendorID = hex(device.idVendor)

     #   print(usb_device_vendorID)

        device_list[usb_device] = usb_device_vendorID

    #print(device_list)
    return device_list
    
def verify_usb(usb_device_list, backup_device, input_device):

    for usb in usb_device_list:
    #    print(usb_device_list[usb])
        if backup_device in usb.lower():
            print('found the backup device')
            backup_usb_device = usb_device_list[usb]
        if input_device.lower() in usb.lower():
            print('found input device')
            input_usb_device = usb_device_list[usb]

    #returns hex(vendorID) of connected USB 
    return backup_usb_device, input_usb_device

def make_udev_rules(backup_vendorID, input_vendorID):
    udev_file = open('/etc/udev/rules.d/10.autobackup.rules', 'w+')
    
    write_str = """SUBSYSTEM="block", ACTION="add", ATTRS{idVendor}==""" + '''"''' + backup_vendorID + '''"''' +""" SYMLINK+="external%n" RUN+="/bin/autobackup.sh" """

    udev_file.write(str(write_str))

    udev_file.close()


if __name__ == "__main__":
    #get backupdevice and input device
    backup_device, input_device = get_configParser()
    
    #get connected usb devices
    usb_device = find_backup()
    
    #validate if backup and input devices are connected
    backup_usb_device, input_usb_device = verify_usb(usb_device, backup_device, input_device)

    #create udev structure
    make_udev_rules(backup_usb_device, input_usb_device)
    
