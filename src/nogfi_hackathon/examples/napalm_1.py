import napalm

ios_driver = napalm.get_network_driver('ios')
huawei_driver = napalm.get_network_driver('huawei_vrp')

ios = {
    'hostname': 'localhost',
    'username': 'admin',
    'password': 'admin',
    'optional_args':{'port': 6001},
}
huawei = {
    'hostname': 'localhost',
    'username': 'admin',
    'password': 'admin',
    'optional_args':{'port': 6002},
}


with ios_driver(**ios) as device:
    facts = device.get_mac_address_table()
    print(facts)

with huawei_driver(**huawei) as device:
    facts = device.get_mac_address_table()
    print(facts)