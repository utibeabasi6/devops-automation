resource "linode_instance" "monitoring" {
    label = "monitoring"
    image = "linode/ubuntu20.04"
    region = "us-southeast"
    type = "g6-nanode-1"
    root_pass = var.root_pass
    tags = [ "managed" ]
}

resource "linode_instance" "logging" {
    label = "logging"
    image = "linode/ubuntu20.04"
    region = "us-southeast"
    type = "g6-nanode-1"
    root_pass = var.root_pass
    tags = [ "managed" ]
}