up: import
	@ansible-playbook -i ansible/inventory.ini ansible/docker.yaml
	@ansible-playbook -i ansible/inventory.ini ansible/logging.yaml
	@ansible-playbook -i ansible/inventory.ini ansible/node_exporter.yaml
	@ansible-playbook -i ansible/inventory.ini ansible/monitoring.yaml

import:
	@chmod +x ./scripts/main.sh && ./scripts/main.sh
	@sleep 20

down:
	@cd terraform && terraform destroy