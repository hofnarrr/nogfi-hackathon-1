from pygnmi.client import gNMIclient
import pathlib
from loguru import logger
import click
from .settings import Settings
import pydantic_core
import sys

current_path = pathlib.Path(__file__).parent.resolve()


def get_settings() -> Settings:
    try:
        settings = Settings()
    except pydantic_core._pydantic_core.ValidationError as e:
        logger.error(f"Settings are not valid: {e}")
        sys.exit(1)
    return settings


def get_lines(filename) -> list[str]:
    try:
        with open(f"{current_path}/files/{filename}") as my_file:
            lines = (my_file.read()).split()
    except FileNotFoundError:
        logger.error(f"File {current_path}/files/{filename} not found")
        sys.exit(1)
    return lines


@click.command()
@click.option(
    "--filename",
    "-n",
    default="sonic-ascii.txt",
    help="filename for some ascii art :) Current options are 'sonic-ascii.txt' and 'sonic-logo.txt'",
)
def main(filename: str):
    settings = get_settings()
    lines = get_lines(filename)

    host = (settings.host, settings.port)

    with gNMIclient(
        target=host,
        username=settings.username,
        password=settings.password,
        skip_verify=True,
    ) as gc:
        config_update = []
        for index, interface_number in enumerate(settings.interface_numbers):
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
        logger.info(result)


if __name__ == "__main__":
    main()
