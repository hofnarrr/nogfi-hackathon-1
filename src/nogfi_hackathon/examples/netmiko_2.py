from netmiko import ConnectHandler

device = {
    'device_type': 'cisco_ios',
    'ip': 'localhost',
    'username': 'admin',
    'password': 'admin',
}


for port in range(6001,6100):
    device["port"] = port
    connection = ConnectHandler(**device)
    sh_ver = connection.send_command('show version', use_textfsm=True)
    print(sh_ver[0]["uptime"])
    sh_ip_arp = connection.send_command('show ip arp', use_textfsm=True)
    ip_addresses = [i["ip_address"] for i in sh_ip_arp]
    print(ip_addresses)
    connection.disconnect()