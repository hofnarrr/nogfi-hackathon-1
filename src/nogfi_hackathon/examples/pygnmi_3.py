from pygnmi.client import gNMIclient
from pprint import pprint

host = ("clab-dell-sonic-test-leaf1", 8080)

config_update = [
    (
        "interfaces/interface[name=Ethernet0]",
        {"config": {"name": "Ethernet0", "enabled": True, "description": "testing666"}},
    )
]


if __name__ == "__main__":
    with gNMIclient(
        target=host, username="admin", password="admin", skip_verify=True
    ) as gc:
        result = gc.set(update=config_update, encoding="json_ietf")

    pprint(result)
