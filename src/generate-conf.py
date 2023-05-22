from jinja2 import Environment, FileSystemLoader
import yaml
from pathlib import Path



conf_files = ["docker-compose.yml", "grafana/datasources/influxdb.yml", "telegraf/telegraf.conf"]
# Open the config.yml file and load its contents into the 'config' variable
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

environment = Environment(loader=FileSystemLoader("templates/"))

for conf_file in conf_files:
    template = environment.get_template(conf_file)

    filename = f"conf/docker-compose.yml"

    content = template.render(
        config
    )
    output_file = Path(conf_file)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(content)
