from netmiko import ConnectHandler
from netutils import time, interface

device = {
    "device_type": "cisco_ios",
    "ip": "localhost",
    "username": "admin",
    "password": "admin",
    "port": 6001,
}

connection = ConnectHandler(**device)
sh_ver = connection.send_command("show version", use_textfsm=True)

uptime_string = sh_ver[0]["uptime"]
print(
    f"Uptime string {uptime_string}, uptime in seconds {time.uptime_string_to_seconds(uptime_string)}"
)

sh_mac = connection.send_command("show mac-address-table", use_textfsm=True)
interface_strings = [i["destination_port"][0] for i in sh_mac]
canonical_interface_names = [
    interface.canonical_interface_name(i) for i in interface_strings
]

print(f"{interface_strings} -> {canonical_interface_names}")

connection.disconnect()
