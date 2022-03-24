#!/bin/sh
set -e pipefall
linodes=`linode-cli linodes list --json --pretty`

echo $linodes | jq -j '[.[] | {name: .label, id: .id, region: .region, ip: .ipv4[0], type: .type, tags: .tags }]' > scripts/servers.json

python3 scripts/import.py scripts/servers.json

cd terraform && terraform apply --auto-approve

cd .. && python3 scripts/gen.py scripts/servers.json
