import httpx
from pprint import pprint
from loguru import logger
import click

url = "https://clab-dell-sonic-test-leaf1:443"  # change this to your switch IP
username = "admin"
password = "admin"

interface_path = "/restconf/data/openconfig-interfaces:interfaces"

auth = httpx.BasicAuth(username=username, password=password)
client = httpx.Client(verify=False, auth=auth)
headers = {
    "accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}


def change_inteface_name(
    interface_name: str = "Ethernet0", description: str = "reserved"
):
    with httpx.Client(verify=False, auth=auth) as client:
        data = {"openconfig-interfaces:description": description}

        desc_path = f"interface={interface_name}/config/description"

        full_path = f"{url}{interface_path}/{desc_path}"
        logger.info(f"Full path {full_path}")

        response = client.get(full_path, headers=headers)

        try:
            logger.info(
                f"Current desc on interface {interface_name}: {response.json()['openconfig-interfaces:description']}"
            )
        except KeyError:
            logger.info(f"interface {interface_name} doesn't have desc")

        response = client.patch(full_path, headers=headers, json=data)
        logger.info(f"interface {interface_name} desc changed to {description}")


@click.command()
@click.option("--name", "-n", default="Ethernet0", help="Interface name")
@click.option("--description", "-d", default="reserved", help="Interface descrption")
def main(name, description):
    change_inteface_name(interface_name=name, description=description)


if __name__ == "__main__":
    main()
