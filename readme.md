HAND-SPEAK - Mano que habla
## Instrucciones

1. Activa el entorno virtual llamado _entorno_.
2. Instala las dependencias del proyecto que se encuentran en requirements.txt.
3. Ejecuta el proyecto con `python app.py`.
4. Abre `http://127.0.0.1:5000` en tu navegador para ver la aplicación en acción.
5. Al momento de estar trabajando con el proyecto si utilizaras una dependencia que no se encuentre en requirements.txt agregala.

## Activa el entorno virtual:

En Windows:
.\entorno\Scripts\activate
En macOS/Linux:
source entorno/bin/activate

## Instalar dependencias

pip install -r requirements.txt

## Agregar dependencias

pip freeze > requirements.txt

# Modelo preentrenado

Debido a limitaciones en el tamaño de archivo de GitHub, el modelo preentrenado se encuentra disponible para su descarga desde Google Drive.

**Descargar modelo**: [Enlace al modelo](https://drive.google.com/file/d/1YSl2AHMni0KBoiMDcMePk59ba8ISMoCR/view?usp=sharing)
A su vez, tambien se deja disponible el enlace del dataset para entrenar su propio modelo.
**Descargar dataset**: [Enlace al modelo](https://www.kaggle.com/datasets/ayuraj/asl-dataset)

Una vez descargado, mueve el archivo a la carpeta correspondiente en tu proyecto.

Modelo sigue enviando datos como si leyera algo. solo y o q manda al liveprediction. Ajustar esto. tambien que vaya armando oraciones.