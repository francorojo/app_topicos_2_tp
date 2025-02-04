#!/bin/sh

python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

 docker build -t api-flask .
 docker run -p 5001:5001 api-flask