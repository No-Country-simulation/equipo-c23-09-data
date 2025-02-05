# HAND-SPEAK - Mano que Habla

## Descripción del Proyecto

HAND-SPEAK es una aplicación web que detecta el lenguaje de señas americano (ASL) y lo traduce a texto en tiempo real. La aplicación utiliza un modelo de machine learning preentrenado para realizar las predicciones y puede manejar tanto imágenes subidas por el usuario como transmisiones de video en vivo a través de la cámara web.

## Características

- **Predicción de Imágenes**: El usuario puede subir imágenes que contengan señas de ASL y obtener la traducción correspondiente.
- **Predicción en Tiempo Real**: La aplicación puede activar la cámara web y realizar predicciones en tiempo real, mostrando las señas detectadas y construyendo oraciones.
- **Manejo de Oraciones**: Las predicciones se agregan a una oración, permitiendo una traducción más fluida y coherente.
- **Eliminación de Predicciones**: El usuario puede eliminar la predicción actual si es incorrecta.

## Requisitos

- Python 3.10 o superior
- Flask
- TensorFlow
- OpenCV
- Flask

## Instalación y Configuración

 1. Crear y Activar el Entorno Virtual

**En Windows:**
python -m venv entorno
.\entorno\Scripts\activate

En macOS/Linux:
python3 -m venv entorno
source entorno/bin/activate

2. Instalar las Dependencias
pip install -r requirements.txt
3. Descargar el Modelo Preentrenado
Debido a limitaciones en el tamaño de archivo de GitHub, el modelo preentrenado se encuentra disponible para su descarga desde Google Drive.

Descargar modelo: Enlace al modelo **https://drive.google.com/file/d/1YSl2AHMni0KBoiMDcMePk59ba8ISMoCR/view**
 A su vez, tambien se deja disponible el enlace del dataset para entrenar su propio modelo. Descargar dataset: Enlace al modelo **https://www.kaggle.com/datasets/ayuraj/asl-dataset**
Mueve el archivo model.keras a la carpeta del proyecto.
-Renombrar el archivo a model.keras y ubicarlo en la carpeta principal.
4. Ejecutar la Aplicación
python app.py
5. Acceder a la Aplicación
Abre tu navegador y navega a http://127.0.0.1:5000 para ver la aplicación en acción.

Uso
Subir Imagenes
Navega a la sección "ASL Sign Prediction".
Haz clic en "Upload an image" y selecciona una imagen que contenga una seña de ASL.
Haz clic en "Predict" para obtener la predicción.
Predicción en Tiempo Real
Navega a la sección "Video Scanner and ASL Prediction".
Haz clic en "Activate Camera" para iniciar la transmisión de video.
Realiza señas de ASL frente a la cámara.
Las predicciones se mostrarán en el cuadro "Live Prediction" y se agregarán a una oración.
Si la predicción es incorrecta, haz clic en "Clear Prediction" para borrar la predicción actual.
Cuando hayas terminado, haz clic en "Stop Camera" para detener la transmisión.


Agregar Dependencias
Si necesitas agregar nuevas dependencias, ejecuta:

pip install <nombre_de_la_dependencia>
Luego, actualiza el archivo requirements.txt:

pip freeze > requirements.txt
Contribuciones

Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

Contacto
Si tienes alguna pregunta o sugerencia, no dudes en contactarme:

Email: karencofrecejas@gmail.com, ianmazzu@gmail.com
GitHub: @karencofre, @ianmazzu
¡Gracias por tu interés en HAND-SPEAK! Esperamos que esta aplicación sea útil.