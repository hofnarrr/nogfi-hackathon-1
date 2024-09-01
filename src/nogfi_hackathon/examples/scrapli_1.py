from scrapli import Scrapli

device = {
    "host": "localhost",
    "auth_username": "admin",
    "auth_password": "admin",
    "auth_strict_key": False,
    "platform": "cisco_iosxe",
    "port": 6001,
}


def main():
    conn = Scrapli(**device)
    conn.open()
    print(conn.get_prompt())
    print(conn.send_command("show version").result + "\n\n")
    conn.close


if __name__ == "__main__":
    main()
