#!/usr/bin python3

import configparser
import subprocess
import usb
import logger
import pyudev
import sys
import os
import re

def get_configParser():
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

def find_backup():
    #Find all USB Devices
    connected_usb = usb.core.find(find_all=True)
    
    #Check if no devices are connected
    if connected_usb == None:
        raise ValueError('No Devices Found.')

    #Loop through connected devices and append to array
    device_list = {}

    for device in connected_usb:
        usb_device = usb.util.get_string(device, device.iManufacturer)
        usb_device = str(usb_device)
        usb_device_vendorID = hex(device.idVendor)
        usb_device_productID = hex(device.idProduct)
        device_list[usb_device] = usb_device_vendorID, usb_device_productID

    print (device_list)
    return device_list
    
def verify_usb(usb_device_list, backup_device, input_device):
    backup_device = backup_device.lower()
    input_device = input_device.lower()
    
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

def make_udev_rules(backup_vendorID, input_vendorID, backup_productID, input_productID, dumper_loc):
    udev_file_source = open('/etc/udev/rules.d/10.autobackup_source.rules', 'w+')
    udev_file_backup = open('/etc/udev/rules.d/11.autobackup_backup.rules', 'w+')
    
    #strip first two characters of hex
    backup_vendorID = backup_vendorID.strip('0x')
    backup_productID = backup_productID.strip('0x')
    input_vendorID = input_vendorID.strip('0x')
    input_productID = input_productID.strip('0x')
    
    write_str_source = """ACTION="add", ATTRS{idVendor}=""" + '''"''' + input_vendorID + '''", ATTRS{idProduct}="''' + input_productID + '''",''' + """ RUN+="/usr/bin/sudo /usr/bin/python3 """ + dumper_loc + '''"'''

    udev_file_source.write(str(write_str_source))

    udev_file_source.close()

    write_str_backup = """ACTION="add", ATTRS{idVendor}=""" + '''"''' + backup_vendorID + '''", ATTRS{idProduct}="''' + backup_productID + '''",''' + """ RUN+="/usr/bin/sudo /usr/bin/python3 """ + dumper_loc + '''"'''

    udev_file_backup.write(str(write_str_backup))

    udev_file_backup.close()

    #reload udev rules
    subprocess.run('udevadm control --reload', shell=True)
    
def mount_usb(dbl, dil, mbl, mil, backup_name, input_name):
    check_path_backup = (mbl + 'backup')
    check_path_input = (mil + 'source')

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
    
    if os.path.exists(check_path_input):
        pass
    else:
        #make dir for mount point
        makedir_input = ('mkdir ' + mil + 'source')
        os.system(makedir_input)

    if os.path.exists(check_path_input):
        #make mount point for input usb
        input_command = ('sudo mount -t auto ' + dil + ' ' + mil + 'source')
        print(input_command)
        os.system(input_command)

def run_autobackup(dev_backup_loc, dev_input_loc, mnt_backup_loc, mnt_input_loc, backup_name, input_name):
    INPUT_SOURCE = (mnt_input_loc + 'source')
    INPUT_DEVICE = (dev_input_loc)
    BACKUP_SOURCE = (mnt_backup_loc + 'backup')
    BACKUP_DEVICE = (dev_backup_loc)
    
    command = ('''rsync -a {0} {1} ''').format(INPUT_SOURCE, BACKUP_SOURCE)

    result = subprocess.run(command, shell=True)
    
    print (result)

def unmount_drives():
    print('unmounting drives...')
    command = ('''umount /mnt/*''')

    subprocess.run(command, shell=True)

    print('Safe to remove drives')


if __name__ == "__main__":
    #get backupdevice and input device configuration settings
    backup_device, input_device, dev_backup_loc, dev_input_loc, mnt_backup_loc, mnt_input_loc, dumper_loc = get_configParser()
    
    #get connected usb devices
    usb_device = find_backup()
    
    #validate if backup and input devices are connected
    backup_usb_device_vendor, input_usb_device_vendor, backup_usb_device_product, input_usb_device_product = verify_usb(usb_device, backup_device, input_device)

    #create udev structure
    make_udev_rules(backup_usb_device_vendor, input_usb_device_vendor, backup_usb_device_product, input_usb_device_product, dumper_loc)
    
    #mount USB
    mount_usb(dev_backup_loc, dev_input_loc, mnt_backup_loc, mnt_input_loc, backup_device, input_device)

    #run backup
    run_autobackup(dev_backup_loc, dev_input_loc, mnt_backup_loc, mnt_input_loc, backup_device, input_device)

    #unmount 
    unmount_drives()
