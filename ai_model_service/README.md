# I Model Service

## Setup

Para setupear el ambiente ejecutar `./setup.sh`

## Desarrollo

Para correr la aplicación de manera simple ejecutar `flask run`.

Si se quiere usar hot-reload ejecutar `flask run --debug`

## Producción

Para ejecutar en un ambiente productivo usamos gunicorn con 4 workers. En caso que se requiera se puede cambiar la cantidad de workers a traves del argumento `-w`. Tener en cuenta que este mismo puede ser modificado a traves del Dockerfile.

Ejemplo el comando `gunicorn -w 4 app:app`

### Configurar modelo

Para configurar los modelos a cargar se deben mapear a traves de docker los siguientes volumenes:

-   ./data/real_state_data_train.tsv.gz el cual debe contener las tripletas para contexto del modelo.
-   ./data/trained_model el cual deberá ser el modelo en sí.

## Test

Para testear el modelo se dejan un archivo con tests funcionales y otro con tests de stress.

### Funcional

`prediction.http` cuenta con ejemplo usando la extensión de HTTP Client de VSC.

Tambien se adjunta `prediction.example.sh` para un ejemplo con curl

### Stress

Se adjunta el archivo `stress_test.sh` para pruebas de stress. Se debe pasar como primer parametro la cantidad de requests que se desean hacer.

