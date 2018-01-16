# Intro
Napalm demo showing how to automate changes to Cisco IOS-XR using the merging configuration.
NAPALM tries to provide a common interface and mechanisms to push configuration and retrieve state data from network devices.

### NAPALM

NAPALM (Network Automation and Programmability Abstraction Layer with Multivendor support) is a Python library that implements a set of functions to interact with different router vendor devices using a unified API.

NAPALM supports several methods to connect to the devices, to manipulate configurations or to retrieve data.


### GitHub Repo's

1. [Napalm](https://github.com/napalm-automation/napalm)

## Install Napalm

Start first by installing the napalm module in python using PIP

```
pip install napalm
```

## Create the JSON file

The json file acts like a backend php/sql db would, this holds the device 

- IP address
- driver (in this case XR)
- username
- password
- rr (reflector or client)

```
{
  "router:1": {
    "IP": "10.94.241.179",
    "type": "iosxr",
    "user": "cisco",
    "password": "cisco",
    "rr": "reflector"
  },
  "router:2": {
    "IP": "10.94.241.171",
    "type": "iosxr",
    "user": "cisco",
    "password": "cisco",
    "rr": "client"
  },
  "router:3": {
    "IP": "10.94.241.172",
    "type": "iosxr",
    "user": "cisco",
    "password": "cisco",
    "rr": "client"
 }
}
```
## Create a cfg file for the route reflector  
This serves as the temaplate use for the changes we want to make for our route reflector. 
Configurations can be replaced entirely or merged (in this case we wil use the merge feature) into the existing device config. 
You can load configuration either from a string or from a file, here we will use the cfg file.

```
router bgp 123
 bgp cluster-id 1
 address-family ipv4 unicast
 !
 neighbor-group rrclients
  remote-as 123
  update-source Loopback0
  address-family ipv4 unicast
   route-reflector-client
  !
 !
 neighbor 192.168.255.1
  use neighbor-group rrclients
 !
 neighbor 192.168.255.2
  use neighbor-group rrclients
```
## Create a cfg file for the route reflector clients
This serves as the temaplate use for the changes we want to make for our route reflector clients
```
router bgp 123
 bgp cluster-id 1
 address-family ipv4 unicast
 !
 neighbor 192.168.255.9
  remote-as 123
  update-source Loopback0
  address-family ipv4 unicast
```


## Running the code

```
python napalm_many_nodes.py
```
You will see you are shown a diff (or if the configurtion is in place already a note saying this is already applied) and 
then the option to eyeball the change, discard or push/commit the change to the devices.

## Rolling back
```
python napalm_many_nodes_rollback.py 
``` 
 This will undo the changes and print a diff showing the changeing being rolled back to each router. Followed by the option to commit


