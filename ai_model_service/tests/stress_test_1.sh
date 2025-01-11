#!/bin/bash


make_request(){
    curl http://localhost:5000/predict -H 'Content-Type: application/json' -s
}

if [[ -n $1 ]];
then
    echo "Stress test started with $1 requests"
else
    echo "Usage: $0 <number_of_requests>"
    exit 1
fi


for i in $(seq 1 $1);
do
    make_request $2 &
done

echo "Stress test ended"
