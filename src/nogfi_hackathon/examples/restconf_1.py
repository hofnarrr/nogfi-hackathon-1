import httpx
from pprint import pprint


url = "https://clab-dell-sonic-test-leaf1:443"
interface_path = "/restconf/data/openconfig-interfaces:interfaces"

auth = httpx.BasicAuth(username="admin", password="admin")
client = httpx.Client(verify=False, auth=auth)
headers = {"accept": "application/yang-data+json", "Content-Type": "application/yang-data+json"}

with httpx.Client(verify=False, auth=auth) as client:
    response = client.get(f"{url}{interface_path}", headers=headers)

    print(response)
    interfaces = response.json()
    #pprint(interfaces)

    for interface in interfaces["openconfig-interfaces:interfaces"]["interface"]:
        print(interface["config"])