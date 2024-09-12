import pprint
from pygnmi.client import gNMIclient

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

def get_if_descs_update():
    updates = []
    for pair in zip(get_ifs(), get_words()):
        updates.append(get_if_update(pair[0], pair[1]))

    return updates

if __name__ == '__main__':
    with gNMIclient(target=hosts[0], username='admin', password='admin1', skip_verify=True) as gc:
        gc.set(update=get_if_descs_update(), encoding='json_ietf')
        s = gc.subscribe_stream(subscribe=if_name_change_sub)
        

