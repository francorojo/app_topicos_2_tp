#!/bin/bash

if [[ $# -ne 7 ]]; then
    echo "Usage: $0 <service> <limit> <offset> <reversed (true/false)> <from (YYYY-MM-DD HH:MM:SS)> <to (YYYY-MM-DD HH:MM:SS)> <tag_type>"
    exit 1
fi

service=$1
limit=$2
offset=$3
reversed=$4
from=$5
to=$6
tag_type=$7

curl -G "http://localhost:5001/logs" \
     --data-urlencode "service=$service" \
     --data-urlencode "limit=$limit" \
     --data-urlencode "offset=$offset" \
     --data-urlencode "reversed=$reversed" \
     --data-urlencode "from=$from" \
     --data-urlencode "to=$to" \
     --data-urlencode "tag_type=$tag_type" | jq
