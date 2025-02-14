#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <property_id>"
    exit 1
fi

property_id=$1

if [[ ! -f "api_key.txt" ]]; then
    echo "API key not found! Please run create_user.sh first."
    exit 1
fi

api_key=$(cat api_key.txt)

curl -s -X POST http://localhost:5003/service \
     -H "Content-Type: application/json" \
     -H "Authorization: $api_key" \
     -d "{\"real_state_index\": $property_id}" | jq
