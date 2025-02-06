#!/bin/bash

# Randomly generated usernames and types
INDEXS=(123451 123452 123453 123454 123455 123456)

# Function to add a random user
add_user() {
    local random_index=${INDEXS[$RANDOM % ${#INDEXS[@]}]}
    curl -X POST "http://localhost:5000/service" \
         -H "Content-Type: application/json" \
         -H "Authorization: 12345678-1234-1234-1234-123456781234" \
         -s -d "{\"real_state_index\": \"$random_index\"}"
}

# Check if number of requests is provided
if [[ -z $1 ]]; then
    echo "Usage: $0 <number_of_requests>"
    exit 1
fi

echo "Starting stress test with $1 requests..."

# Loop for making requests in parallel
for i in $(seq 1 $1); do
    make_request &
done

echo "Stress test ended"
