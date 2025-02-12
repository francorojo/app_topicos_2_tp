# Log Service

## Init

Ejecutar el comando `gunicorn -w 1 app:app`

## Test

Ejecutar stress tests.

## Uso de logs

### Parámetros de la Solicitud

A continuación, se describen los parámetros disponibles para filtrar los registros:

🏷️ 1. service (obligatorio)
**Descripción**: Especifica el servicio cuyos logs se desean consultar.
**Ejemplo**: "service=auth" filtra solo los registros del servicio de autenticación.

🔢 2. limit (opcional)
**Descripción**: Define la cantidad máxima de registros que se devolverán en la respuesta.
Valor por defecto: 20
**Ejemplo**: "limit=50" retorna hasta 50 registros.

🔄 3. offset (opcional)
**Descripción**: Omite los primeros n registros antes de devolver la respuesta. Útil para paginación.
Valor por defecto: 0
**Ejemplo**: "offset=10" omite los primeros 10 registros y devuelve los siguientes.

🔃 4. reversed (opcional)
**Descripción**: Indica si los registros deben mostrarse en orden inverso (del más reciente al más antiguo).
Valores posibles: true o false
Valor por defecto: false
**Ejemplo**: "reversed=true" devuelve los registros más recientes primero.

📅 5. from (opcional)
**Descripción**: Define la fecha y hora de inicio para filtrar los registros.
Formato: YYYY-MM-DD HH:MM:SS
**Ejemplo**: "from=2025-01-01 00:00:00" devuelve solo registros desde el 1 de enero de 2025 en adelante.

📅 6. to (opcional)
**Descripción**: Define la fecha y hora de fin para filtrar los registros.
Formato: YYYY-MM-DD HH:MM:SS
**Ejemplo**: "to=2025-01-31 23:59:59" devuelve solo registros hasta el 31 de enero de 2025.

🏷️ 7. tag_type (opcional)
**Descripción**: Filtra los registros según una etiqueta específica, útil para categorizar eventos.
**Ejemplo**: "tag_type=tag_example" devuelve solo los registros con la etiqueta tag_example.

