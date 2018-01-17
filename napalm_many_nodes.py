#!/usr/bin/python
#
#
import argparse
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

def make_changes(device_list, auto=False):
    yes = {'yes','y', 'ye', ''}
    no = {'no','n'}
    if auto:
        choice = 'yes'
    else:
        choice = raw_input('Deploy all devices yes or no: ').lower()
        
    if choice not in yes and no:
        print("Please respond with 'yes' or 'no': ")

    for device in device_list:
        if (choice in yes) or auto:
            print("Applying changes {}...".format(device[1]))
            #print(dir(device))
            device[0].commit_config()
            device[0].close()

        elif choice in no:
            print("Discarding changes {}...".format(device[1]))
            device[0].discard_config()
            device[0].close()


if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='NAPALM Deployment')
    parser.add_argument('--inventory', dest='inventory', help='sum the integers (default: find the max)')
    parser.add_argument('--auto', dest='auto', action='store_true', help='do not prompt for confirmation before deployment')
    args = parser.parse_args()

    print("Intializing NAPALM run with {}".format(args.inventory))
    if args.auto:
        print("Running in auto-deploy mode!")

    # # get command line parameter
    # if len(sys.argv) != 1:
    #     merge_device("Usage: merge_conf hostname conf_file")
    #     hostname = sys.argv[1]
    #     conf_file = sys.argv[2]
    #
    # load device parameter database

    try:
        with open(args.inventory, "r") as f:
            device_data = json.load(f)
    except (ValueError, IOError, OSError) as err:
        merge_device("Could not read the 'devices' file:", err)
    #

    # router list for files to be added to client or reflector

    router_list = [router for router in device_data]
    router_list.sort()
    device_list = []

    for router in router_list:
        if device_data[router]['rr'] == "client":
            update_router_config(router, 'client_file.cfg')

        else:
            update_router_config(router, 'reflector_file.cfg')


    if len(device_list) > 0:
        if args.auto:
            make_changes(device_list, auto=True)
        else:
            make_changes(device_list)
