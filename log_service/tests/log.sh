#!/bin/bash

curl -X POST http://localhost:8000/log \
     -H "Content-Type: application/json" \
     -d '{
           "service": "auth - app",
           "message": "logged",
           "tag_type": "tag_example"
         }'
