terraform {
  required_providers {
    linode = {
      source  = "linode/linode"
      # version = "..."
    }
  }
}

provider "linode" {
    token = var.linode_token
}