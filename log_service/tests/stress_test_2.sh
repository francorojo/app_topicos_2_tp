#!/bin/bash


make_request(){
    curl http://localhost:8000/log -H 'Content-Type: application/json' -d "{\"service\": \"app\", \"message\":\"$1\"}" -s
}

if [[ -n $1 ]];
then
    echo "Stress test started with $1 requests"
else
    echo "Usage: $0 <number_of_requests>"
    exit 1
fi

if [[ -n $2 ]];
then
    echo "First Message: $2"
else
    echo "First message not provided"
    exit 1
fi

if [[ -n $3 ]];
then
    echo "Second Message: $3"
else
    echo "Second message not provided"
    exit 1
fi


for i in $(seq 1 $1);
do
    make_request $2 &
    make_request $3 &
done

echo "Stress test ended"
