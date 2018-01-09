#!/usr/bin/python
#
#
import sys
import json
from napalm import get_network_driver

def merge_device(*msg_list):
    """ abort program with error message """
    error_msg = ' '.join(str(x) for x in msg_list)
    sys.exit(error_msg.rstrip("\n\r"))

def make_changes(device_list):
    #while True:        
    yes = {'yes','y', 'ye', ''}
    no = {'no','n'}
    choice = raw_input('Deploy all devices yes or no [or q to quit]: ').lower()
        
    if choice == 'q':
        print
        print ("Exiting...")
        sys.exit()

        
    if choice not in yes and no:
        print("Please respond with 'yes' or 'no' [q to quit]:")
    
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


# Making a list of routers/keys from convert json.

router_list = [router for router in device_data]
device_list = []

for router in router_list:
    driver = get_network_driver(device_data[router]['type'])
    device = driver(hostname=device_data[router]['IP'],
        password=device_data[router]['password'],
        username=device_data[router]['user'] )
    device.open()
    device.load_merge_candidate(filename='prefix_list.cfg')
    diffs = device.compare_config()
    print '='*10,'{}'.format(router),'='*10
    
    if diffs == "":
        print("Configuration already applied")
        device.discard_config()
        device.close()
    else:
        print(diffs)
        device_list.append([device,router])

if len(device_list) > 0:
    make_changes(device_list)





