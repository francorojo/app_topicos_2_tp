#!/bin/bash

# List of real_state_index values
INDEXES=(
  393231
  360467
  393246
  294943
  294945
  294947
  393251
  294951
  393255
)

# Function to make a request with a random index from the list
make_request() {
    local random_index=${INDEXES[$RANDOM % ${#INDEXES[@]}]}
    curl http://localhost:5000/predict -H 'Content-Type: application/json' -s -d "{\"real_state_index\": $random_index }"
}

# Check if number of requests is provided
if [[ -n $1 ]]; then
    echo "Stress test started with $1 requests"
else
    echo "Usage: $0 <number_of_requests>"
    exit 1
fi

# Loop for making requests in parallel
for i in $(seq 1 $1); do
    make_request &
done

echo "Stress test ended"
