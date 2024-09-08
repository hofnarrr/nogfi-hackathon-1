from pygnmi.client import gNMIclient
from pprint import pprint
import pathlib
from loguru import logger
from intspan import intspan
import click

current_path = pathlib.Path(__file__).parent.resolve()

host = ("clab-dell-sonic-test-leaf1", 8080)

interface_numbers = list(intspan("0-48,52,56,60,64,68,72,76"))


@click.command()
@click.option(
    "--filename",
    "-n",
    default="sonic-ascii",
    help="filename for some ascii art :) Current options are 'sonic-ascii.txt' and 'sonic-logo.txt'",
)
def main(filename):
    with open(f"{current_path}/files/{filename}") as my_file:
        lines = (my_file.read()).split()

    with gNMIclient(
        target=host, username="admin", password="admin", skip_verify=True
    ) as gc:
        config_update = []
        for index, interface_number in enumerate(interface_numbers):
            try:
                line = lines[index]
            except IndexError:
                line = ""
            logger.info(f"Updating interface Ethernet{interface_number}")
            path = f"openconfig-interfaces:interfaces/interface[name=Ethernet{interface_number}]/config"
            config = {
                "openconfig-interfaces:config": {
                    "description": line,
                }
            }
            config_update.append((path, config))
        result = gc.set(update=config_update, encoding="json_ietf")

    # pprint(result)


if __name__ == "__main__":
    main()
