output "monitoring_ip" {
    value = linode_instance.monitoring.ipv4
}

output "logging_ip" {
    value = linode_instance.logging.ipv4
}