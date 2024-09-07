from jinja2 import Environment, FileSystemLoader
from loguru import logger

import pathlib

current_path = pathlib.Path(__file__).parent.resolve()


# Define interface parameters
interface_data = {
    "interface": "GigabitEthernet0/1",
    "description": "Uplink to core switch",
    "ip_address": "192.168.1.10",
    "subnet_mask": "255.255.255.0",
}

# Set up the Jinja2 environment
file_loader = FileSystemLoader(
    f"{current_path}/templates"
)  # Directory where template is stored
env = Environment(loader=file_loader)

# Load the Jinja2 template
template = env.get_template("cisco_ios_interface.j2")

# Render the configuration with the provided data
output = template.render(interface_data)

# Print the rendered configuration
logger.info(output)

# Optionally, you could save it to a file
with open(f"{current_path}/configs/generated_interface_config.txt", "w") as f:
    f.write(output)
