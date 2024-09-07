from netmiko import ConnectHandler
import netmiko
import click
import pathlib
from loguru import logger
import random

# This script will run dead slow and there are many ways it can be improved

script_path = pathlib.Path(__file__).absolute().parent

device = {
    "device_type": "dell_sonic_ssh",
    "ip": "clab-dell-sonic-test-leaf1",
    "username": "admin",
    "password": "admin",
}


def read_story_to_a_list(storyname: str):
    story_file = f"{script_path.parent}/stories/{storyname}"
    try:
        with open(story_file) as f:
            s = f.read()
            story_list = s.split()
            return story_list
    except FileNotFoundError as e:
        logger.info(f"File not found {story_file}")
        return []


def change_interface_description(interface_name: str, description: str):
    connection = ConnectHandler(**device)
    interfaces = connection.send_command(
        "show interface status",
        use_textfsm=True,
        textfsm_template=f"{script_path}/dell_sonic_ssh_show_interface_status.textfsm",
    )
    interface = [i for i in interfaces if i["interface"] == interface_name][0]
    if interface["description"] != description:
        logger.info(
            f"Interface {interface_name} description must be changed: {interface['description']} -> {description}"
        )
        commands = [
            "configure",
            f"interface {interface_name}",
            f"description {description }",
            "end",
            "write mem",
        ]
        connection.send_config_set(commands)
        connection.disconnect()
        return True
    return False


def get_all_interfaces():
    logger.info(f"Getting interfaces form {device['ip']}")
    try:
        with ConnectHandler(**device) as connection:
            interfaces = connection.send_command(
                "show interface status",
                use_textfsm=True,
                textfsm_template=f"{script_path}/dell_sonic_ssh_show_interface_status.textfsm",
            )
            return [i["interface"] for i in interfaces]
    except netmiko.exceptions.NetmikoTimeoutException as e:
        logger.info(f"Error: {e}")
        return []


@click.command()
@click.option("--storyname", "-n", default="aliens.txt", help="Name of the story")
def main(storyname):
    logger.info(f"Script path: {script_path}")
    logger.info(f"getting the story")
    story = read_story_to_a_list(storyname)
    if story:
        logger.info(f"Story as list: {story}")
        interface_names = get_all_interfaces()
        logger.info(f"Interface names: {interface_names}")
        interface_and_description = list(zip(interface_names, story))
        random.shuffle(interface_and_description)
        for interface_name in interface_and_description:
            change_status = change_interface_description(
                interface_name=interface_name[0], description=interface_name[1]
            )
            if change_status:
                logger.info(
                    f"Interface {interface_name[0]} description changed to '{interface_name[1]}'!"
                )
            else:
                logger.info(
                    f"Interface {interface_name[0]} description already correct!"
                )


if __name__ == "__main__":
    main()
