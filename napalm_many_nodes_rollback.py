#!/usr/bin/python
#
#
import sys
import json
from napalm import get_network_driver

# abort program with error message

def merge_device(*msg_list):
    error_msg = ' '.join(str(x) for x in msg_list)
    sys.exit(error_msg.rstrip("\n\r"))

# function for device information

def update_router_config(router, filename):
    driver = get_network_driver(device_data[router]['type'])
    device = driver(hostname=device_data[router]['IP'],
                    password=device_data[router]['password'],
                    username=device_data[router]['user'])

    device.open()
    device.load_merge_candidate(filename=filename)
    diffs = device.compare_config()
    print '='*10,'{}'.format(router),'='*10
    if diffs == "":
        print("Configuration already applied")
        device.discard_config()
        device.close()
    else:
        print(diffs)
        device_list.append([device,router])

# function for making changes on diff

def make_changes(device_list):        
    yes = {'yes','y', 'ye', ''}
    no = {'no','n'}
    choice = raw_input('Deploy all devices yes or no: ').lower()
           
    if choice not in yes and no:
        print("Please respond with 'yes' or 'no': ")
    
    for device in device_list:
        if choice in yes:
            print("Applying changes {}...".format(device[1]))
            #print(dir(device))
            device[0].commit_config()
            device[0].close()

        elif choice in no:
            print("Discarding changes {}...".format(device[1]))
            device[0].discard_config()
            device[0].close() 


# get command line parameter
if len(sys.argv) != 1:
    merge_device("Usage: merge_conf hostname conf_file")
    hostname = sys.argv[1]
    conf_file = sys.argv[2]

# load device parameter database
try:
    with open("devices.json", "r") as f:
        device_data = json.load(f)
except (ValueError, IOError, OSError) as err:
    merge_device("Could not read the 'devices' file:", err)


# router list for files to be added to client or reflector

router_list = [router for router in device_data]
router_list.sort()
device_list = []

for router in router_list:
    update_router_config(router, 'no_bgp.cfg')


if len(device_list) > 0:
    make_changes(device_list)
