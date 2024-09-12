import json
import pprint
from pygnmi.client import gNMIclient
import sys

hosts = [
        ('172.21.5.40', '8080'),
        ('172.21.5.41', '8080'),
        ('172.21.5.42', '8080')
]

if_name_change_sub = {
    "subscription": [
        {
            "path": "openconfig-interfaces:interfaces/interface[name=*]/config",
            "mode": "on_change",
        },
    ],
    "use_aliases": False,
    "mode": "stream",
    "encoding": "json_ietf",
}

def get_words():
    with open('story.txt', 'r') as story:
        words = story.readline().strip().replace(',', '').replace('.', '').split(' ')
        return words

def get_ifs():
    with open('interfaces.txt', 'r') as interfacelist:
        interfaces = interfacelist.readline().strip().split(' ')
        return interfaces

def get_if_update(interface, desc):
    return (
        f'openconfig-interfaces:interfaces/interface[name={interface}]/config',
        {
            "openconfig-interfaces:config": {
                "description": f"{desc}",
                "enabled": True,
                "name": f"{interface}",
                "type": "iana-if-type:ethernetCsmacd",
            }
        },
    )

def get_if_descs():
    return zip(get_ifs(), get_words())

def get_if_descs_update():
    updates = []
    for pair in get_if_descs():
        updates.append(get_if_update(pair[0], pair[1]))

    return updates

if __name__ == '__main__':
    if len(sys.argv) > 1:
        host_index = int(sys.argv[1])
    else:
        host_index = 0
    with gNMIclient(target=hosts[host_index], username='admin', password='admin1', skip_verify=True) as gc:
        gc.set(update=get_if_descs_update(), encoding='json_ietf')
        sub = gc.subscribe_stream(subscribe=if_name_change_sub)
        
        for event in sub:
            intf = event['update']['prefix'].split('=')[1].split(']')[0]
            desc = event['update']['update'][0]['val']
            print(f'if {intf} desc changed to: {desc}')

            if 'Ethernet' not in intf: continue

            idx = get_ifs().index(intf)
            newdesc = get_words()[idx]
            
            upd = [get_if_update(intf, newdesc)]
            gc.set(update=upd, encoding='json_ietf')
            print(f'UPDATED {intf} DESC to {newdesc}')

