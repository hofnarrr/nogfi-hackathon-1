import asyncio

from scrapli.driver.core import AsyncIOSXEDriver

IOSDEVICE1 = {
    "host": "localhost",
    "auth_username": "admin",
    "auth_password": "admin",
    "auth_strict_key": False,
    "port": 6001,
    "transport": "asyncssh",
    "driver": AsyncIOSXEDriver,
}

IOSDEVICE2 = {
    "host": "localhost",
    "auth_username": "admin",
    "auth_password": "admin",
    "auth_strict_key": False,
    "port": 6002,
    "transport": "asyncssh",
    "driver": AsyncIOSXEDriver,
}

DEVICES = [IOSDEVICE1, IOSDEVICE2]


async def gather_version(device):
    """Simple function to open a connection and get some data"""
    driver = device.pop("driver")
    conn = driver(**device)
    await conn.open()
    prompt_result = await conn.get_prompt()
    version_result = await conn.send_command("show version")
    await conn.close()
    return prompt_result, version_result


async def main():
    """Function to gather coroutines, await them and print results"""
    coroutines = [gather_version(device) for device in DEVICES]
    results = await asyncio.gather(*coroutines)
    for result in results:
        print(f"device prompt: {result[0]}")
        print(f"device show version: {result[1].result}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
