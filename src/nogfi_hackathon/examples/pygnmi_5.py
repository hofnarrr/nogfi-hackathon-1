from pygnmi.client import gNMIclient, telemetryParser
from pprint import pprint

host = ("clab-dell-sonic-test-leaf1", 8080)

subscribe = {
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


if __name__ == "__main__":
    with gNMIclient(
        target=host, username="admin", password="admin", skip_verify=True
    ) as gc:
        telemetry_stream = gc.subscribe_stream(subscribe=subscribe)

        for telemetry_entry in telemetry_stream:
            print(telemetry_entry)

