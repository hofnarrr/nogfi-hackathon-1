# Tasks

## Netmiko

These examples assume that you have fakenos running with 100 cisco ios simulations

```bash
# rye run fakenos --inventory src/nogfi_hackathon/fakenos/inventory_100_ios.yaml
Initiating FakeNOS
INFO:fakenos.plugins.utils.cli:Initiating FakeNOS
INFO:fakenos.core.fakenos:The following devices has been initiated: ['ios68', 'ios14', 'ios20', 'ios61', 'ios74', 'ios32', 'ios90', 'ios87', 'ios99', 'ios48', 'ios6', 'ios57', 'ios69', 'ios78', 'ios24', 'ios39', 'ios63', 'ios0', 'ios9', 'ios33', 'ios22', 'ios5', 'ios64', 'ios53', 'ios52', 'ios36', 'ios8', 'ios44', 'ios51', 'ios7', 'ios18', 'ios71', 'ios81', 'ios47', 'ios13', 'ios58', 'ios2', 'ios21', 'ios80', 'ios83', 'ios17', 'ios16', 'ios42', 'ios98', 'ios26', 'ios27', 'ios35', 'ios76', 'ios37', 'ios3', 'ios43', 'ios89', 'ios31', 'ios28', 'ios86', 'ios70', 'ios95', 'ios93', 'ios45', 'ios25', 'ios88', 'ios82', 'ios56', 'ios75', 'ios55', 'ios96', 'ios62', 'ios92', 'ios4', 'ios65', 'ios79', 'ios12', 'ios19', 'ios15', 'ios41', 'ios60', 'ios94', 'ios59', 'ios97', 'ios34', 'ios49', 'ios73', 'ios29', 'ios67', 'ios72', 'ios84', 'ios85', 'ios10', 'ios54', 'ios11', 'ios46', 'ios50', 'ios66', 'ios1', 'ios38', 'ios77', 'ios91', 'ios23', 'ios30', 'ios40']
INFO:fakenos.core.fakenos:Device ios68 is running on port 6001
INFO:fakenos.core.fakenos:Device ios14 is running on port 6002
INFO:fakenos.core.fakenos:Device ios20 is running on port 6003
INFO:fakenos.core.fakenos:Device ios61 is running on port 6004
```


1. Connect to a device with Netmiko and collect information
    1. parse the device uptime from show version on ios device
    1. parse all ip addresses from 'show ip arp' command
1. collect the same information from 100 ios devices
    1. how long does it take? How can it be improved?
1. try out different parsers
    1. textfsm, genie
1. Collect same data with multi vendor inventory

## Textfsm parsing

1. Create textfsm parser for following output
    ```bash
    Legend: Mac Address: * = address not valid
    
     Domain   Vlan/SrvcId        Mac Address            Type         Protocol     Operation          Interface
    --------+--------------+---------------------+----------------+------------+--------------+------------------------
       VLAN    656            00:00:00:00:f5:00     learned          ---          bridging       1/35
       VLAN    656            00:00:00:00:f5:01     learned          ---          bridging       1/35
    ```
    
    so that the data will be printed out in following format
    
    ```python
    [
    	{
    		"domain": "VLAN",
    		"interface": "1/35",
    		"mac_address": "00:00:00:00:f5:00",
    		"operation": "bridging",
    		"protocol": "---",
    		"type": "learned",
    		"vlan": "656"
    	},
    	{
    		"domain": "VLAN",
    		"interface": "1/35",
    		"mac_address": "00:00:00:00:f5:01",
    		"operation": "bridging",
    		"protocol": "---",
    		"type": "learned",
    		"vlan": "656"
    	}
    ]
    ```
    
    
    
    You can use https://textfsm.nornir.tech for trying it out.

1. Try out parsing some other command or data which is not included on the existing parsers

## Netutils

1. Try out the netutilsmodule for the netmiko output, https://github.com/networktocode/netutils
    1. convert time to seconds, convert interface names etc

## Napalm

Try out data collection with napalm. Please note that data collection with fakenos simulated devices will have issues as support for different commands varies. There's an example code 'examples/napalm_1.py' with fakenos inventory 'fakenos/inventory_napalm.yaml'. Modify the code by adding devices from virtual lab.

## Scrapli

While netmiko uses paramiko for handling the SSH connection, scrapli uses asyncssh. This makes it very fast. Compare the result with netmiko setting up the 100 ios devices with fakenos.

You can follow how the ssh connections are built with tcpdump

```bash
# tcpdump -i lo portrange 6000-6100 -n
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on lo, link-type EN10MB (Ethernet), snapshot length 262144 bytes
09:07:08.661313 IP 127.0.0.1.42528 > 127.0.0.1.6001: Flags [S], seq 2005705929, win 65495, options [mss 65495,sackOK,TS val 986549099 ecr 0,nop,wscale 7], length 0
09:07:08.661331 IP 127.0.0.1.6001 > 127.0.0.1.42528: Flags [S.], seq 1111788761, ack 2005705930, win 65483, options [mss 65495,sackOK,TS val 986549099 ecr 986549099,nop,wscale 7], length 0
09:07:08.661346 IP 127.0.0.1.42528 > 127.0.0.1.6001: Flags [.], ack 1, win 512, options [nop,nop,TS val 986549099 ecr 986549099], length 0
09:07:08.663671 IP 127.0.0.1.34408 > 127.0.0.1.6007: Flags [S], seq 686090579, win 65495, options [mss 65495,sackOK,TS val 986549101 ecr 0,nop,wscale 7], length 0
09:07:08.663696 IP 127.0.0.1.6007 > 127.0.0.1.34408: Flags [S.], seq 2551154655, ack 686090580, win 65483, options [mss 65495,sackOK,TS val 986549101 ecr 986549101,nop,wscale 7], length 0
09:07:08.663714 IP 127.0.0.1.34408 > 127.0.0.1.6007: Flags [.], ack 1, win 512, options [nop,nop,TS val 986549101 ecr 986549101], length 0
09:07:08.666643 IP 127.0.0.1.39818 > 127.0.0.1.6010: Flags [S], seq 1660499834, win 65495, options [mss 65495,sackOK,TS val 986549104 ecr 0,nop,wscale 7], length 0
09:07:08.666665 IP 127.0.0.1.6010 > 127.0.0.1.39818: Flags [S.], seq 2201196217, ack 1660499835, win 65483, options [mss 65495,sackOK,TS val 986549104 ecr 986549104,nop,wscale 7], length 0
09:07:08.666686 IP 127.0.0.1.39818 > 127.0.0.1.6010: Flags [.], ack 1, win 512, options [nop,nop,TS val 986549104 ecr 986549104], length 0
09:07:08.667742 IP 127.0.0.1.48734 > 127.0.0.1.6009: Flags [S], seq 4002595400, win 65495, options [mss 65495,sackOK,TS val 986549105 ecr 0,nop,wscale 7], length 0
09:07:08.667755 IP 127.0.0.1.6009 > 127.0.0.1.48734: Flags [S.], seq 2413743074, ack 4002595401, win 65483, options [mss 65495,sackOK,TS val 986549105 ecr 986549105,nop,wscale 7], length 0
09:07:08.667766 IP 127.0.0.1.48734 > 127.0.0.1.6009: Flags [.], ack 1, win 512, options [nop,nop,TS val 986549105 ecr 986549105], length 0
09:07:08.667888 IP 127.0.0.1.51866 > 127.0.0.1.6014: Flags [S], seq 1294552701, win 65495, options [mss 65495,sackOK,TS val 986549105 ecr 0,nop,wscale 7], length 0
09:07:08.667896 IP 127.0.0.1.6014 > 127.0.0.1.51866: Flags [S.], seq 1055880580, ack 1294552702, win 65483, options [mss 65495,sackOK,TS val 986549105 ecr 986549105,nop,wscale 7], length 0
09:07:08.667904 IP 127.0.0.1.51866 > 127.0.0.1.6014: Flags [.], ack 1, win 512, options [nop,nop,TS val 986549105 ecr 986549105], length 0
09:07:08.668010 IP 127.0.0.1.45370 > 127.0.0.1.6011: Flags [S], seq 2277702348, win 65495, options [mss 65495,sackOK,TS val 986549105 ecr 0,nop,wscale 7], length 0
```


## REST API

This example is with Dell Sonic REST API. The API swagger docs can be found from the switch

```bash
https://<switch ip>/ui/
```

The access can be tested with curl

```bash
# curl -k -X GET "https://clab-dell-sonic-test-leaf1:443/restconf/data/openconfig-interfaces:interfaces" -H "accept: application/yang-data+json" -u "admin:admin"
{"openconfig-interfaces:interfaces":{"interface":[{"config":{"description":"testing","enabled":true,"mtu":9100,"name":"Ethernet0","type":"iana-if-type:ethernetCsmacd"},"dhcpv4-snooping-trust":{"config":{"dhcpv4-snooping-trust":"DISABLE"},"state":{"dhcpv4-snooping-trust":"DISABLE"}},"dhcpv6-snooping-trust":{"config":{"dhcpv6-snooping-trust":"DISABLE"},"state":{"dhcpv6-snooping-trust":"DISABLE"}},"openconfig-if-ethernet:ethernet":{"config":{"openconfig-if-ethernet-ext2:advertised-speed":"","auto-negotiate":false,"openconfig-if-ethernet-ext2:port-fec":"openconfig-platform-ext:FEC_FC","port-speed":"openconfig-if-ethernet:SPEED_25GB","openconfig-if-ethernet-ext2:standalone-link-training":false},"openconfig-if-ethernet-phy-ext:phy-mon-status":{"phy-mon-fields":[{"state":{"last-change":"2024-09-01T06:56:13Z+00:00","last-status":"nok","phy-m
```

or via the provided examples examples/sonic_rest_api_1.py etc

# Jinja2

There's an example jinja2 template in examples/templates

```jinja
interface {{ interface }}
 description {{ description }}
 ip address {{ ip_address }} {{ subnet_mask }}
 no shutdown
```

and jinja2_1.py script. The current script writes configuration for single interface and stores that to a file in configs directory.

Modify the script/template so that it creates the configuration to interfaces GigabitEthernet0/1 to GigabitEthernet0/24 with so that description has text 'nogfi\-<interface number\>, i.e. interface GigabitEthernet0/1 should have description of 'nogfi-1' The IP address allocation logic '192.168.\<interface number\>.10/24', i.e GigabitEthernet0/1 should have IP 192.168.1.10/24.

Modify the script/templates so that every other interface is shutdown, every 3rd has no description and every 4th has no IP address.


## (py)gnmi


gnmic locally on the sonic switch
```bash
admin@sonic:~$ docker run --network host --rm ghcr.io/openconfig/gnmic --address localhost:8080 -u admin -p admin --skip-verify -e JSON_IETF get --path /system/state/boot-time
[
  {
    "source": "localhost:8080",
    "timestamp": 1725391905543477038,
    "time": "2024-09-03T19:31:45.543477038Z",
    "updates": [
      {
        "Path": "openconfig-system:system/state/boot-time",
        "values": {
          "openconfig-system:system/state/boot-time": {
            "openconfig-system:boot-time": "1725389701000000000"
          }
        }
      }
    ]
  }
]
```
gnmic

```bash
# gnmic -a clab-dell-sonic-test-leaf1:8080 -u admin -p admin --skip-verify get --path /system/state/boot-time -e json_ietf
[
  {
    "source": "clab-dell-sonic-test-leaf1:8080",
    "timestamp": 1725391928783164007,
    "time": "2024-09-03T22:32:08.783164007+03:00",
    "updates": [
      {
        "Path": "openconfig-system:system/state/boot-time",
        "values": {
          "openconfig-system:system/state/boot-time": {
            "openconfig-system:boot-time": "1725389701000000000"
          }
        }
      }
    ]
  }
]
```
pygnmicli

```bash
pygnmicli -t clab-dell-sonic-test-leaf1:8080 -u admin -p admin  --skip-verify -o get -x /interfaces/interface[name=Ethernet0]/state/counters -e json_ietf
Cannot get Common Name: list index out of range
ssl_target_name_override is applied, should be used for testing only!
Collecting Capabilities...
Collection of Capabilities is successfull
Selected encoding 'json' based on capabilities
Collecting Capabilities...
Collection of Capabilities is successfull
Doing get request to ('clab-dell-sonic-test-leaf1', 8080)...
Collecting info from requested paths (Get operation)...
{
    "notification": [
        {
            "timestamp": 1725398542049882888,
            "prefix": null,
            "alias": null,
            "atomic": false,
            "update": [
                {
                    "path": "openconfig-interfaces:interfaces/interface[name=Ethernet0]/state/counters",
                    "val": {
                        "openconfig-interfaces:counters": {
                            "in-bits-per-second": "0",
                            "in-broadcast-pkts": "0",
                            "in-discards": "0",
                            "in-errors": "0",
                            "in-multicast-pkts": "0",
                            "in-octets": "0",
                            "in-octets-per-second": "0",
                            "in-pkts": "0",
                            "in-pkts-per-second": "0",
                            "in-unicast-pkts": "0",
                            "in-utilization": 0,
                            "last-clear": "0",
                            "out-bits-per-second": "0",
                            "out-broadcast-pkts": "0",
                            "out-discards": "0",
                            "out-errors": "0",
                            "out-multicast-pkts": "0",
                            "out-octets": "0",
                            "out-octets-per-second": "0",
                            "out-pkts": "0",
                            "out-pkts-per-second": "0",
                            "out-unicast-pkts": "0",
                            "out-utilization": 0
                        }
                    }
                }
            ]
        }
    ]
}
```

```bash
# pygnmicli -t clab-dell-sonic-test-leaf1:8080 -u admin -p admin  --skip-verify -o get -x /interfaces/interface[name=Ethernet0]/config -e json_ietf
Cannot get Common Name: list index out of range
ssl_target_name_override is applied, should be used for testing only!
Collecting Capabilities...
Collection of Capabilities is successfull
Selected encoding 'json' based on capabilities
Collecting Capabilities...
Collection of Capabilities is successfull
Doing get request to ('clab-dell-sonic-test-leaf1', 8080)...
Collecting info from requested paths (Get operation)...
{
    "notification": [
        {
            "timestamp": 1725398593255766783,
            "prefix": null,
            "alias": null,
            "atomic": false,
            "update": [
                {
                    "path": "openconfig-interfaces:interfaces/interface[name=Ethernet0]/config",
                    "val": {
                        "openconfig-interfaces:config": {
                            "description": "In",
                            "enabled": true,
                            "mtu": 9100,
                            "name": "Ethernet0",
                            "type": "iana-if-type:ethernetCsmacd"
                        }
                    }
                }
            ]
        }
    ]
}
```


Python example

```python
from pygnmi.client import gNMIclient
from pprint import pprint

host = ('clab-dell-sonic-test-leaf1', 8080)

if __name__ == '__main__':
    with gNMIclient(target=host, username='admin', password='admin', skip_verify=True) as gc:
        result = gc.get(path=['/system/state/boot-time'], encoding='json_ietf')
         
    pprint(result)
```



```bash
# python src/nogfi_hackathon/examples/pygnmi_1.py 
Cannot get Common Name: list index out of range
ssl_target_name_override is applied, should be used for testing only!
{'notification': [{'alias': None,
                   'atomic': False,
                   'prefix': None,
                   'timestamp': 1725394540053831523,
                   'update': [{'path': 'openconfig-system:system/state/boot-time',
                               'val': {'openconfig-system:boot-time': '1725389702000000000'}}]}]}
```




## Nornir