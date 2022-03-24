#!/usr/env/python3

import sys
import json
import os
from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape


def generate_template(instances):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape()
    )
    template = env.get_template("main.tf.j2")
    print("Generating terraform file".center(80, "-"))
    return template.render(instances=instances)

if len(sys.argv) < 2:
    sys.exit("No json file passed")

with open(sys.argv[1]) as f:
    instance_ids = [instance for instance in json.load(f) if "managed" not in instance["tags"]]

terraform_template = generate_template(instance_ids)
with open("terraform/main.tf", "w") as f:
    f.write(terraform_template)

for instance in instance_ids:
    os.system(f"cd terraform && terraform import linode_instance.{instance['name']} {instance['id']}")

