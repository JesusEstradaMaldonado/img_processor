# Usar una imagen base de Python 3.10 (slim para hacerla ligera)
FROM python:3.10-slim

# Instalar dependencias del sistema necesarias para Pillow y herramientas de desarrollo
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    build-essential \
    gcc

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requerimientos y las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código al contenedor
COPY . .

# Exponer el puerto 5000 para Flask
EXPOSE 5000

# Ejecutar la aplicación
CMD ["python", "app.py"]
