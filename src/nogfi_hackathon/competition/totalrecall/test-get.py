import os
import json

from pygnmi.client import gNMIclient, telemetryParser

SONIC_HOST = os.getenv("SONIC_HOST", "172.21.5.40")
SONIC_PORT = os.getenv("SONIC_PORT", "8080")
SONIC_USERNAME = os.getenv("SONIC_USERNAME", "admin")
SONIC_PASSWORD = os.getenv("SONIC_PASSWORD", "admin1")

host = (SONIC_HOST, SONIC_PORT)

paths = [
    "interfaces/interface[name=Ethernet1]/config/",
]

with gNMIclient(
    target=host, username=SONIC_USERNAME, password=SONIC_PASSWORD, skip_verify=True
) as gc:
    raw_data = gc.get(path=paths, encoding="json_ietf")
    print(json.dumps(raw_data, sort_keys=True, indent=2))
