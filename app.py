from flask import Flask, request, send_file, jsonify, render_template, send_from_directory
import os
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import uuid  # Para generar nombres únicos de archivos
from datetime import datetime  # Para añadir la fecha y hora de procesamiento

app = Flask(__name__)

# Configuración del directorio de almacenamiento de imágenes
UPLOAD_FOLDER = 'static/images/'
PROCESSED_FOLDER = 'static/processed_images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Crear las carpetas si no existen
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

# Lista para almacenar detalles de imágenes procesadas
image_history = []

# Función para validar archivos permitidos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Endpoint para subir una imagen y procesarla
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    action = request.form.get('action')
    size = request.form.get('size')
    degrees = request.form.get('degrees')
    brightness = request.form.get('brightness')

    # Generar un nombre único para la imagen original y guardarla
    original_filename = str(uuid.uuid4()) + "_" + file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
    file.save(file_path)

    # Procesar la imagen y guardarla en la carpeta de imágenes procesadas
    processed_filename = process_image(file_path, action, size, degrees, brightness)

    # Guardar en el historial de imágenes procesadas
    image_history.append({
        "filename": processed_filename,
        "action": action,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    return send_file(processed_filename, as_attachment=True)

# Función para procesar la imagen según la acción seleccionada
def process_image(image_path, action, size=None, degrees=None, brightness=None):
    image = Image.open(image_path)
    
    # Generar un nombre único para la imagen procesada
    processed_filename = str(uuid.uuid4()) + "_" + os.path.basename(image_path)
    processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
    
    if action == 'grayscale':
        image = ImageOps.grayscale(image)
    
    elif action == 'resize' and size:
        width, height = map(int, size.split('x'))
        image = image.resize((width, height))
    
    elif action == 'rotate' and degrees:
        image = image.rotate(float(degrees))
    
    elif action == 'brightness' and brightness:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(float(brightness))
    
    elif action == 'invert':
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image = ImageOps.invert(image)
    
    elif action == 'blur':
        image = image.filter(ImageFilter.GaussianBlur(3))
    
    elif action == 'mirror':
        image = ImageOps.mirror(image)
    
    elif action == 'flip':
        image = ImageOps.flip(image)
    
    # Guardar la imagen procesada
    image.save(processed_path)
    
    return processed_path

# Endpoint para listar las imágenes procesadas
@app.route('/images', methods=['GET'])
def list_images():
    return jsonify({"images": image_history})

# Endpoint para servir las imágenes procesadas
@app.route('/static/processed_images/<filename>')
def serve_processed_image(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


