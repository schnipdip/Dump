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
        #print (device)
        usb_device = usb.util.get_string(device, device.iManufacturer)
        usb_device_vendorID = hex(device.idVendor)

        device_list[usb_device] = usb_device_vendorID

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

def make_udev_rules(backup_vendorID, input_vendorID, dumper_loc):
    udev_file = open('/etc/udev/rules.d/10.autobackup.rules', 'w+')
    
    write_str = """SUBSYSTEM="block", ACTION="add", ATTRS{idVendor}==""" + '''"''' + backup_vendorID + '''"''' +""" SYMLINK+="external%n" RUN+="/bin/python3 """ + dumper_loc + '''"''' 

    udev_file.write(str(write_str))

    udev_file.close()

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
    
    command = ('''/usr/bin/rsync -a {0} {1} ''').format(INPUT_SOURCE, BACKUP_SOURCE)

    result = subprocess.run(command, shell=True)
    
    print (result)

def unmount_drives():
    print('unmounting drives')
    command = ('''/usr/bin/umount /mnt/*''')

    subprocess.run(command, shell=True)



if __name__ == "__main__":
    #get backupdevice and input device configuration settings
    backup_device, input_device, dev_backup_loc, dev_input_loc, mnt_backup_loc, mnt_input_loc, dumper_loc = get_configParser()
    
    #get connected usb devices
    usb_device = find_backup()
    
    #validate if backup and input devices are connected
    backup_usb_device, input_usb_device = verify_usb(usb_device, backup_device, input_device)

    #create udev structure
    make_udev_rules(backup_usb_device, input_usb_device, dumper_loc)
    
    #mount USB
    mount_usb(dev_backup_loc, dev_input_loc, mnt_backup_loc, mnt_input_loc, backup_device, input_device)

    #run backup
    run_autobackup(dev_backup_loc, dev_input_loc, mnt_backup_loc, mnt_input_loc, backup_device, input_device)

    #unmount 
    unmount_drives()
