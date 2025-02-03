import os
import cv2
import numpy as np
from flask import Flask, request, render_template, redirect, url_for, jsonify, Response
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import io
import time

# Establecer la variable de entorno para desactivar oneDNN_OPTS
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = Flask(__name__)

# Configuración para la carpeta de subidas
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Cargar el modelo
model = load_model('model.keras')

# Parámetros de entrada del modelo
image_size = 200
img_channel = 3
n_classes = 36

# Diccionario para mapear las clases
categories = {
    0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9",
    10: "a", 11: "b", 12: "c", 13: "d", 14: "e", 15: "f", 16: "g", 17: "h", 18: "i", 19: "j",
    20: "k", 21: "l", 22: "m", 23: "n", 24: "o", 25: "p", 26: "q", 27: "r", 28: "s", 29: "t",
    30: "u", 31: "v", 32: "w", 33: "x", 34: "y", 35: "z",
}

# Variable de estado para controlar si la cámara está activa
camera_active = False

# Variable global para almacenar el texto predicho
predicted_text = ""
predicted_sentence = []

# Tiempo de espera para considerar una letra finalizada (en segundos)
WAIT_TIME = 3

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar la subida de archivos
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return f"File uploaded successfully: {filepath}", 200

# Ruta para hacer predicciones
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return "No image part", 400
    file = request.files['image']
    if file.filename == '':
        return "No selected image", 400
    if file:
        img_bytes = file.read()
        img = load_img(io.BytesIO(img_bytes), target_size=(image_size, image_size))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction, axis=1)

        return jsonify({'class': categories[predicted_class[0]]})

# Ruta para activar la cámara
@app.route('/start_camera', methods=['POST'])
def start_camera():
    global camera_active, predicted_text, predicted_sentence
    camera_active = True
    predicted_text = ""
    predicted_sentence = []
    return jsonify({'status': 'Camera activated'})

# Ruta para detener la cámara
@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    global camera_active, predicted_text, predicted_sentence
    camera_active = False
    predicted_text = ""
    predicted_sentence = []
    return jsonify({'status': 'Camera deactivated'})

# Ruta para capturar video en tiempo real y enviar predicciones
@app.route('/live_prediction')
def live_prediction():
    def gen_predictions():
        global predicted_text, predicted_sentence
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        last_detection_time = time.time()
        while camera_active:
            success, frame = cap.read()
            if not success:
                break
            else:
                # Convertir el frame a un formato compatible
                img_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
                img = load_img(io.BytesIO(img_bytes), target_size=(image_size, image_size))
                img_array = img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)
                img_array = img_array / 255.0

                prediction = model.predict(img_array)
                predicted_class = np.argmax(prediction, axis=1)
                label = categories[predicted_class[0]]

                # Si la confianza es menor al umbral, consideramos que no hay manos
                if max(prediction[0]) < 0.1:
                    if time.time() - last_detection_time > WAIT_TIME:
                        predicted_text = ""
                    last_detection_time = time.time()
                else:
                    # Actualizar el texto predicho
                    if label not in predicted_text:
                        predicted_text += label
                        predicted_sentence.append(label)
                    last_detection_time = time.time()

                yield f"data: {' '.join(predicted_sentence)}\n\n"

    return Response(gen_predictions(), mimetype='text/event-stream')

# Ruta para eliminar la predicción
@app.route('/clear_prediction', methods=['POST'])
def clear_prediction():
    global predicted_text, predicted_sentence
    predicted_text = ""
    predicted_sentence = []
    return jsonify({'status': 'Prediction cleared'})

if __name__ == '__main__':
    app.run(debug=True)