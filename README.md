# Trabajo práctico Tópicos 2

## Introducción

El trabajo practico consistió en armar una arquitectura donde se disponibiliza un modelo de IA el cual nos permitirá obtener, a partir de un universo de propiedades conocidas, las 10 propiedades más similares.

## Setup

Preparación del ambiente para interactuar

1. Se deben buildear las imagenes de docker. Para esto ejectuar el script `build_all.sh`
2. Ejecutar `docker compose up -d` para dejar preparado el ambiente

## Pruebas

1. Crear usuario para obtener API key

```
curl -X POST http://localhost:5002/users \
     -H "Content-Type: application/json" \
     -d '{"username": "<username>", "type": "PREMIUM"}'
```

Tambien se puede utilizar el tipo **FREEMIUM** para usuarios más limitados.

**RECORDAR** copiar y guardar la API key ya que una vez creada no se podrá volver a consultar. Para las predicciones sobre el servicio de _api_core_ es necesario enviar el header **Authorization** con la API key como valor para que se autorice la predicción.

2. Consultar propiedades disponibles para predecir similares

```
curl -X GET http://localhost:5000/properties
```

Tomar uno de los valores de las propiedades para utilizar en la próxima consulta.

3. Predecir las 10 propiedas más similares

```
curl -X POST http://localhost:5003/service \
     -H "Content-Type: application/json" \
     -H "Authorization: <api_key>" \
     -d '{"real_state_index": <property_id>}'
```

4. Consultar los logs para ver el registro de las acciones

```
curl -G "http://localhost:5001/logs" \
     --data-urlencode "service=auth" \
     --data-urlencode "limit=20" \
     --data-urlencode "offset=5" \
     --data-urlencode "reversed=true" \
     --data-urlencode "from=2025-01-01 00:00:00" \
     --data-urlencode "to=2025-01-31 23:59:59" \
     --data-urlencode "tag_type=tag_example"

```

5. Consultar reiteradas veces en una ventana de tiempo para ver como un usuario FREEMIUM o PREMIUM cuentan con distinta cantidad de intentos.

### Carpeta Tests

En la carpeta `tests` encontrarán scripts para probar con los servicios expuestos en el docker compose.

Está automatizado el uso de la API key dentro de un file para simplificar las pruebas.
