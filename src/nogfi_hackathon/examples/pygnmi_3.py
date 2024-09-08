from pygnmi.client import gNMIclient
from pprint import pprint

host = ("clab-dell-sonic-test-leaf1", 8080)

config_update = [
    (
        "openconfig-interfaces:interfaces/interface[name=Ethernet0]/config",
        {
            "openconfig-interfaces:config": {
                "description": "test-desc1",
                "enabled": True,
                "name": "Ethernet0",
                "type": "iana-if-type:ethernetCsmacd",
            }
        },
    )
]


if __name__ == "__main__":
    with gNMIclient(
        target=host, username="admin", password="admin", skip_verify=True
    ) as gc:
        result = gc.get(
            path=["openconfig-interfaces:interfaces/interface[name=Ethernet0]/config"],
            encoding="json_ietf",
        )
        pprint(result)
        result = gc.set(update=config_update, encoding="json_ietf")

    pprint(result)
