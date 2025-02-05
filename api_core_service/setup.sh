#!/bin/sh

python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

brew install memcached
brew services start memcached