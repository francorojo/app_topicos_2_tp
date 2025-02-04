# Utilice la imagen oficial de Python 3.8 slim como imagen base
FROM python:3.9-slim 

# Establezca el directorio de trabajo dentro del contenedor
WORKDIR /api-flask 

# Copie los archivos y directorios necesarios en el contenedor
COPY api.py /api-flask/ 
COPY requirements.txt /api-flask/ 

# Actualizar pip e instalar las dependencias de Python
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt 

# Exponer el puerto 5001 para la aplicación Flask
EXPOSE 5001 

# Definir el comando para ejecutar la aplicación Flask
CMD [ "flask" , "--app" , "api" , "run" , "--host=0.0.0.0" , "--port=5001" ]
