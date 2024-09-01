from netmiko import ConnectHandler

device = {
    'device_type': 'cisco_ios',
    'ip': 'localhost',
    'username': 'admin',
    'password': 'admin',
    'port': 6001
}

connection = ConnectHandler(**device)
sh_ver = connection.send_command('show version')
print(sh_ver)
sh_ip_arp = connection.send_command('show ip arp')
print(sh_ip_arp)
connection.disconnect()