# Utilice la imagen oficial de Python 3.8 slim como imagen base
FROM python:3.9-slim 

# Install Memcached
RUN apt-get update && apt-get install -y memcached && rm -rf /var/lib/apt/lists/*

# Establezca el directorio de trabajo dentro del contenedor
WORKDIR /app


COPY requirements.txt . 

# Actualizar pip e instalar las dependencias de Python
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt 

RUN pip install gunicorn

# Copie los archivos y directorios necesarios en el contenedor
COPY app app 

# Exponer el puerto 5000 para la aplicación Flask
EXPOSE 5000

# Create a non-root user and group
RUN groupadd -r myuser && useradd -r -g myuser myuser

# Change to the non-root user
USER myuser


# Start Memcached and define the command to run the Flask application
CMD ["sh", "-c", "memcached -d && gunicorn -w 4 app:app --bind 0.0.0.0:8000"]
