#!/bin/bash

# Randomly generated usernames and types
USERNAMES=("alice" "bob" "charlie" "dave" "eve")
TYPES=("admin" "guest" "member")

# Function to add a random user
add_user() {
    local random_username=${USERNAMES[$RANDOM % ${#USERNAMES[@]}]}
    local random_type=${TYPES[$RANDOM % ${#TYPES[@]}]}
    curl -X POST "http://localhost:5000/users" \
         -H "Content-Type: application/json" \
         -s -d "{\"username\": \"$random_username\", \"type\": \"$random_type\"}"
}

# Function to fetch all users
get_users() {
    curl -X GET "http://localhost:5000/users" -s
}

# Function to fetch a user by random ID (you may need to update valid IDs)
get_user_by_id() {
    local user_id=$1  # User ID passed as argument
    curl -X GET "http://localhost:5000/users/$user_id" -s
}

# Check if number of requests is provided
if [[ -z $1 ]]; then
    echo "Usage: $0 <number_of_requests>"
    exit 1
fi

echo "Starting stress test with $1 requests..."

# Run test in parallel
for i in $(seq 1 $1); do
    case $((RANDOM % 3)) in
        0) add_user & ;;      # 33% of requests will be POST /users
        1) get_users & ;;     # 33% of requests will be GET /users
        2) get_user_by_id "$((RANDOM % 100 + 1))" & ;;  # 33% will GET a user by ID
    esac
done

echo "Stress test completed!"
