# app_topicos_2_tp
App using microservices and integration with ai model.

Steps
cd myproject
python3 -m venv .venv
. .venv/bin/activate
pip install Flask
pip install Flask-Limiter
pip install simple-rest-client
pip install pymemcache

arch -arm64 brew install memcached
brew install memcached
brew services start memcached

flask --app hello run
