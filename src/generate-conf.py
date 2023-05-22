from jinja2 import Environment, FileSystemLoader
import yaml
from pathlib import Path

# List of configuration files
conf_files = [
    "docker-compose.yml",
    "grafana/datasources/influxdb.yml",
    "grafana/dashboards/dashboard.yml",
    "grafana/dashboards/cisco-catalyst-9800_clients-stats.json",
    "grafana/dashboards/cisco-meraki_global-stats.json",
    "telegraf/telegraf.conf"
]

# Open the config.yml file and load its contents into the 'config' variable
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

# Create a Jinja2 environment and specify the template loader
environment = Environment(loader=FileSystemLoader("templates/"))

# Iterate over each configuration file
for conf_file in conf_files:
    # Get the template for the current configuration file
    template = environment.get_template(conf_file)
    
    # Render the template with the 'config' variable
    content = template.render(config)
    
    # Create the output file path
    output_file = Path(conf_file)
    
    # Create any necessary parent directories for the output file
    output_file.parent.mkdir(exist_ok=True, parents=True)
    
    # Write the rendered content to the output file
    output_file.write_text(content)