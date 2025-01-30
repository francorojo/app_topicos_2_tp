#!/bin/bash

if [[ -z "$1" ]]; then
echo "Pasar indice como parametro. Ej. prediction.example.sh 1234"
exit 1
fi

curl http://localhost:5000/predict -H 'Content-Type: application/json' -s -d "{\"real_state_index\": $1 }"
