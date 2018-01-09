# Intro
Napalm demo showing how to automate changes to Cisco IOS-XR using the merging configuration.
NAPALM tries to provide a common interface and mechanisms to push configuration and retrieve state data from network devices.

## Create the JSON

The json file acts like a backend php/sql db would, this holds the device 

- IP address
- driver (in this case XR)
- username
- password

```{
  "router:1": {
    "IP": "[ip address]",
    "type": "iosxr",
    "user": "[add here]",
    "password": "[add here]"
  },
  "router:2": {
    "IP": "[ip address]6",
    "type": "iosxr",
    "user": "[add here]",
    "password": "[add here]"
  }
}
```
## Create a cfg file, 
This serves as the temaplate use for the changes we want to make, for example building a new prefix set
```
prefix-set AGGREGATES-ORLONGER
  27.115.64.0/19 ge 19,
  125.10.61.0/24 ge 24,
  125.10.62.0/24 ge 24,
  125.10.63.0/24 ge 24,
  125.10.128.0/24 ge 24,
  125.10.129.0/24 ge 24,
  125.10.131.0/24 ge 24,
end-set
```

## Python code

On the Python code you can see the sections where the json and cfg files are called

```
# load device parameter database
try:
    with open("devices.json", "r") as f:
```

```
device.load_merge_candidate(filename='config_file.cfg')
```

## Running the code

```
Python napalm_many_nodes.py
```
You will see you are shown a diff (or if the configurtion is in place already a note saying this is already applied) and then the option to eyeball the change, discard or push/commit the change to the devices.
