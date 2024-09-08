# Modules
import datetime
from nornir.init_nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_pygnmi.tasks import gnmi_get


# Statics
PATH = [f"openconfig-interfaces:interfaces/interface[name=Ethernet{interface_number}]/config" for interface_number in range(0,48)]


# Body
if __name__ == "__main__":
    # Get initial timestamp
    start_time = datetime.datetime.now()
    print(f"Execution started at {start_time}")

    # Initialise Nornir
    nrn = InitNornir(
        runner={
            "plugin": "threaded",
            "options": {
                "num_workers": 100,
            },
        },
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": "inventory/hosts.yaml",
            },
        },
    )
    hosts = nrn.inventory.hosts
    print(hosts)
    # Perform action
    result = nrn.run(task=gnmi_get, path=PATH, encoding="json_ietf")
    # print_result(result)

    print(result.keys())
    # print(result["sw1"][0].result)

    for i in result["sw1"][0].result["notification"]:
        print(i["update"][0]["val"]["openconfig-interfaces:config"]["description"], i["update"][0]["val"]["openconfig-interfaces:config"]["name"])

    # # Get final timestamp
    # end_time = datetime.datetime.now()
    # print(f"Execution took {end_time - start_time} and completed at {end_time}")
