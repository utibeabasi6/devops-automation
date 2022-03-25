#!/usr/env/python3

import subprocess
import sys
import json
import os
from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape

def gen_prom_config(instances):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape()
    )
    template = env.get_template("prometheus.yml.j2")
    print("Generating prometheus compose file".center(80, "-"))
    return template.render(instances=instances)

def generate_ansible_inventory(monitored, monitoring, logging):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape()
    )
    template = env.get_template("inventory.ini.j2")
    print("Generating inventory file".center(80, "-"))
    return template.render(monitored=monitored, monitoring=monitoring, logging=logging)

def gen_promtail(logging):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape()
    )
    template = env.get_template("promtail_config.yaml.j2")
    print("Generating promtail config file".center(80, "-"))
    return template.render(logging=logging)

def gen_systemd(name, command, description="A simple systemd file"):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape()
    )
    template = env.get_template("systemd.service.j2")
    print(f"Generating Systemd file for {name}".center(80, "-"))
    return template.render(name=name, description=description, command=command)

# Check if the JSON file containing the IP addresses was passed in
if len(sys.argv) < 2:
    sys.exit("No json file passed")

with open(sys.argv[1]) as f:
    instance_ids = [instance for instance in json.load(f) if "managed" not in instance["tags"]]

# Get the IP address of the monitoring and logging server
monitoring_command = subprocess.Popen("cd terraform && terraform output --json monitoring_ip | jq '.[0]'", stdout=subprocess.PIPE, shell=True)
logging_command = subprocess.Popen("cd terraform && terraform output --json logging_ip | jq '.[0]'", stdout=subprocess.PIPE, shell=True)

(monitoring_ip, err) = monitoring_command.communicate()
(logging_ip, err) = logging_command.communicate()

monitoring_ip = monitoring_ip.decode('utf-8').split("\n")[0].split('"')[1]
logging_ip = logging_ip.decode('utf-8').split("\n")[0].split('"')[1]

# Generate the ansible inventory file
with open("ansible/inventory.ini", "w") as f:
    f.write(generate_ansible_inventory([instance["ip"] for instance in instance_ids], monitoring_ip, logging_ip))

# Generate the docker-compose file for promtail and pass in the ip address of the logging server
with open("ansible/files/promtail/promtail_config.yaml", "w") as f:
    f.write(gen_promtail(logging_ip))

# Generate a service file for node exporter
with open("ansible/files/node_exporter/node_exporter.service", "w") as f:
    f.write(gen_systemd("node_exporter", "/usr/local/bin/node_exporter", description="A systemd service for node exporter"))

# Generate a service file for promtail
with open("ansible/files/promtail/promtail.service", "w") as f:
    f.write(gen_systemd("promtail", "/app/start.sh", description="A systemd service for promtail"))

# Generate a service file for monitoring
with open("ansible/files/monitoring/monitoring.service", "w") as f:
    f.write(gen_systemd("monitoring", "/app/start.sh", description="A systemd service for monitoring"))

# Generate a service file for logging
with open("ansible/files/logging/logging.service", "w") as f:
    f.write(gen_systemd("logging", "/app/start.sh", description="A systemd service for logging"))

with open("ansible/files/monitoring/prometheus/prometheus.yml", "w") as f:
    f.write(gen_prom_config(instance_ids))