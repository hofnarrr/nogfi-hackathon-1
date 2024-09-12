import pprint
from pygnmi.client import gNMIclient

hosts = [
        ('172.21.5.40', '8080'),
        ('172.21.5.41', '8080'),
        ('172.21.5.42', '8080')
        ]


sub = {
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


if __name__ == '__main__':
    with gNMIclient(target=hosts[0], username='admin', password='admin1', skip_verify=True) as gc:
        s = gc.subscribe_stream(subscribe=sub)

        for e in s:
            pprint.pp(e)
