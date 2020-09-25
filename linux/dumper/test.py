import configparser
import usb.core
import usb.util

def get_configParser():
    config = configparser.ConfigParser()
    config.read('../settings.ini')

    return config


def find_backup():
    config = get_configParser()
    backup_device = config['settings']['backup_device_name']
        
    #Find all USB Devices
    connected_usb = usb.core.find(find_all=True)

    #Check if no devices are connected
    #if connected_usb == None:
    #    raise ValueError('No Devices Found.')

    #Loop through connected devices and append to array
    #device_list = []

    for device in connected_usb:
    #    print(device)
        test1 = usb.util.get_string(device, device.iManufacturer)
        print(test1) 
    return connected_usb

if __name__ == "__main__":
    test = find_backup()
    print(test)
