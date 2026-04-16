# 06-Recetas

Recetas AI es una aplicación web desarrollada con Streamlit que genera recetas de cocina simples a partir de una lista de ingredientes. La aplicación utiliza los SDK de LLMs de proveedores como Google y Groq para crear el nombre, los ingredientes con medidas, las instrucciones, notas y la información nutricional de la receta. Las recetas generadas se pueden guardar y consultar posteriormente.

## Características

- Interfaz web interactiva construida con Streamlit.
- Generación de recetas (nombre, ingredientes, instrucciones, notas) mediante LLMs.
- Cálculo de información nutricional (calorías, proteínas, carbohidratos, grasas) usando LLMs.
- Generación de prompts para imágenes de las recetas.
- Creación de imágenes para las recetas utilizando el modelo de generación de imágenes de Google.
- Selección dinámica entre modelos de Google y Groq para la generación de texto.
- Uso de los SDKs específicos de cada proveedor de LLM.
- Almacenamiento de recetas generadas (incluyendo metadatos e imagen) en formato JSON y archivos de imagen.
- Carga y visualización de recetas guardadas.
- Comparativa visual de calorías entre las recetas guardadas.
- Código modular y organizado para facilitar su comprensión y extensión.

## Estructura

- `main.py`: Punto de entrada de la aplicación. Define la interfaz principal de usuario con Streamlit.
- `apoyo_app.py`: Contiene la lógica principal de la aplicación, incluyendo el manejo del estado de la sesión, la interacción con los módulos de LLM para generar recetas e imágenes, y la gestión de la visualización de las recetas.
- `apoyo_archivos.py`: Proporciona funciones para leer, escribir y gestionar los archivos JSON de las recetas guardadas en el directorio `recetas/`.
- `apoyo_llm_groq_sdk.py`: Módulo para interactuar con la API de Groq utilizando su SDK, para la generación de texto.
- `apoyo_llm_google_sdk.py`: Módulo para interactuar con la API de Google (Gemini) utilizando su SDK, tanto para la generación de texto como para la generación de imágenes.
- `config.py`: Archivo de configuración donde se definen las claves de API, los modelos de LLM a utilizar, los nombres de los directorios para datos e imágenes, y otros parámetros.
- `recetas/`: Carpeta donde se almacenan los archivos JSON de cada receta generada. (Definido en `config.DIR_ARCHIVOS`)
- `recetas-img/`: Carpeta donde se guardan las imágenes generadas para las recetas. (Definido en `config.DIR_IMAGENES`)
- `prompts/`: Carpeta que contiene los archivos de texto con las plantillas de prompts utilizadas para interactuar con los LLMs. (Definido en `config.DIR_PROMPTS`)
- `requirements.txt`: (No provisto, pero se asume) Listado de las dependencias de Python necesarias para ejecutar la aplicación.

## Instalación y Ejecución

1.  **Requisitos previos:**
    *   Python 3.10 o superior instalado.
    *   Claves de API válidas para Google (Gemini) y/o Groq, según los proveedores que desees utilizar.

2.  **Instala las dependencias:**

    pip install -r requirements.txt      

5.  **Configura tus claves y parámetros:**
    *   Edita el archivo `config.py` para introducir tus claves de API (`LLM_GROQ_API_KEY`, `LLM_GOOGLE_API_KEY`).

6.  **Ejecuta la aplicación:**
    Navega hasta el directorio raíz del proyecto en tu terminal y ejecuta:

    streamlit run main.py


7.  **Usa la aplicación:**
    Se abrirá una nueva pestaña en tu navegador web con la interfaz de la aplicación "Recetas AI". Ingresa los ingredientes, selecciona un proveedor y genera tus recetas.

## Notas

- Las recetas generadas se guardan como archivos JSON en la carpeta `recetas/`.
- Las imágenes de las recetas se guardan en la carpeta `recetas-img/`.
- Este proyecto está diseñado con fines educativos y como demostración de las capacidades de GenAI para la creación de contenido estructurado y visual.

---
📝 GenAI Dev Workshop 2025 · alfredo.de.regil