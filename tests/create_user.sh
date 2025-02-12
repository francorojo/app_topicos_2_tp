#!/bin/bash

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <username> <user_type (PREMIUM/FREEMIUM)>"
    exit 1
fi

username=$1
user_type=$2

response=$(curl -s -X POST http://localhost:5002/users \
     -H "Content-Type: application/json" \
     -d "{\"username\": \"$username\", \"type\": \"$user_type\"}")

api_key=$(echo "$response" | jq -r '.user.api_key')

if [[ "$api_key" != "null" && -n "$api_key" ]]; then
    echo "API Key: $api_key"
    echo "$api_key" > api_key.txt
    echo "API Key saved to api_key.txt"
fi
