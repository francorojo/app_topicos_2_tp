# Api Core Service
Aplicación encargada de realizar la integracion de los diferentes servicios.

## Init
Utilizar el script setup.sh
En caso de no funcionar el comando: brew install memcached
Es necesario utilizar: arch -arm64 brew install memcached
Luego de finalizar el uso se debe correr el comando: brew services stop memcached

Ejecutar el comando `flask --app hello run --port number`

o
docker build -t api-flask .    
docker run -p 5000:5000 api-flask
