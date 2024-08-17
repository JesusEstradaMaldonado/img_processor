## Instrucciones para configurar y ejecutar la aplicación localmente

### Requisitos previos:
- Python 3.x
- pip (el gestor de paquetes de Python)
- Docker (opcional)

### 1. Clonar el repositorio:
Clona este repositorio en tu máquina local:

git clone https://github.com/tuusuario/tu-repositorio.git
cd tu-repositorio

## 2.Instala las dependencias necesarias usando pip
pip install -r requirements.txt

## Una vez instaladas las dependencias, puedes ejecutar la aplicación
python app.py
-------------------------------------------------------------------

## Instrucciones para ejecutar la aplicación con Docker (opcional)

### 1. Construir la imagen Docker:
En la raíz del proyecto, ejecuta el siguiente comando para construir la imagen Docker:
docker build -t img_processor .

## 2. Ejecutar el contenedor Docker:
docker run -p 5000:5000 img_processor

## 3. Usar la aplicación en Docker:
Abre tu navegador y dirígete a http://localhost:5000/.
-------------------------------------------------------------------

## EndPoints del API:
## 1. POST /upload:
Sube una imagen para procesarla.

## Parámetros:

image: archivo de imagen (png, jpg, jpeg, gif).
action: acción a realizar (grayscale, rotate, resize, etc.).
## Ejemplo de Respuesta: 

{
  "message": "Image processed",
  "filename": "nombre_de_imagen_procesada.jpg"
}

## 2. GET /images:
Lista de imágenes procesadas.

## Ejemplo de respuesta:
[
  {
    "filename": "12345_grayscale.jpg",
    "action": "grayscale",
    "date": "2024-08-17 15:30:00"
  },

  {
    "filename": "12346_rotate.jpg",
    "action": "rotate",
    "date": "2024-08-17 15:40:00"
  }
]

