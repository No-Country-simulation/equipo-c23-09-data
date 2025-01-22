import os
import cv2
import numpy as np
from flask import Flask, request, render_template, redirect, url_for, jsonify, Response
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

# Configuración para la carpeta de subidas
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Cargar el modelo
model = load_model('model.keras')

# Diccionario para mapear las clases
categories = {
    0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9",
    10: "a", 11: "b", 12: "c", 13: "d", 14: "e", 15: "f", 16: "g", 17: "h", 18: "i", 19: "j",
    20: "k", 21: "l", 22: "m", 23: "n", 24: "o", 25: "p", 26: "q", 27: "r", 28: "s", 29: "t",
    30: "u", 31: "v", 32: "w", 33: "x", 34: "y", 35: "z",
}

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
        img = image.load_img(file, target_size=(64, 64))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction, axis=1)

        return jsonify({'class': categories[predicted_class[0]]})

# Ruta para capturar video en tiempo real
def gen_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Procesar el frame
            img = cv2.resize(frame, (64, 64))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0

            prediction = model.predict(img_array)
            predicted_class = np.argmax(prediction, axis=1)
            label = categories[predicted_class[0]]

            # Dibujar el label en el frame
            cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
