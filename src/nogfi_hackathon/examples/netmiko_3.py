from netmiko import ConnectHandler
import json


device = {
    "device_type": "cisco_ios",
    "ip": "localhost",
    "username": "admin",
    "password": "admin",
    "port": 6001,
}

connection = ConnectHandler(**device)
sh_ver = connection.send_command("show version", use_genie=True)
print(json.dumps(sh_ver, indent=4, sort_keys=True))
sh_ip_arp = connection.send_command("show ip arp", use_genie=True)
print(json.dumps(sh_ip_arp, indent=4, sort_keys=True))
connection.disconnect()
