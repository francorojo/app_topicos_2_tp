# Utilice la imagen oficial de Python 3.8 slim como imagen base
FROM python:3.8-slim 

# Establezca el directorio de trabajo dentro del contenedor
WORKDIR /api-flask 

# Copie los archivos y directorios necesarios en el contenedor
COPY /app . 
COPY requirements.txt . 

# Actualizar pip e instalar las dependencias de Python
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt 

# Install Memcached
RUN apt-get update && apt-get install -y memcached && rm -rf /var/lib/apt/lists/*

# Exponer el puerto 5000 para la aplicación Flask
EXPOSE 5000

# Create a non-root user and group
RUN groupadd -r myuser && useradd -r -g myuser myuser

# Change to the non-root user
USER myuser

# Start Memcached and define the command to run the Flask application
CMD ["sh", "-c", "memcached -d && flask --app api run --host=0.0.0.0 --port=5000"]
