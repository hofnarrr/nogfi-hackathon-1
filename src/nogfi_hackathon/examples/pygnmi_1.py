from pygnmi.client import gNMIclient
from pprint import pprint

host = ("clab-dell-sonic-test-leaf1", 8080)

if __name__ == "__main__":
    with gNMIclient(
        target=host, username="admin", password="admin", skip_verify=True
    ) as gc:
        result = gc.get(path=["/system/state/boot-time"], encoding="json_ietf")

    pprint(result)
