import os
import json

from pygnmi.client import gNMIclient, telemetryParser

with open('story.txt', 'r') as story:
    words = story.readline().replace(',', '').replace('.', '').split(' ')
    print(words)

with open('interfaces.txt', 'r') as interfacelist:
    interfaces = interfacelist.readline().split(' ')
    print(interfaces)

assert len(words) == len(interfaces)

SONIC_HOST = os.getenv("SONIC_HOST", "172.21.5.40")
SONIC_PORT = os.getenv("SONIC_PORT", "8080")
SONIC_USERNAME = os.getenv("SONIC_USERNAME", "admin")
SONIC_PASSWORD = os.getenv("SONIC_PASSWORD", "admin1")

host = (SONIC_HOST, SONIC_PORT)

u = [
    (
        "openconfig-interfaces:interfaces/interface[name=Ethernet1]/config",
        {
            "openconfig-interfaces:config": {
                "description": "test-desc3",
                "enabled": True,
                "name": "Ethernet1",
                "type": "iana-if-type:ethernetCsmacd",
            }
        },
    ),
    (
        "openconfig-interfaces:interfaces/interface[name=Ethernet2]/config",
        {
            "openconfig-interfaces:config": {
                "description": "test-desc4",
                "enabled": True,
                "name": "Ethernet2",
                "type": "iana-if-type:ethernetCsmacd",
            }
        },
    )

]

with gNMIclient(
    target=host, username=SONIC_USERNAME, password=SONIC_PASSWORD, skip_verify=True
) as gc:
    result = gc.set(update=u, encoding="json_ietf")
    print(result)

