# apoyo_llm_google_sdk.py - GenAI Dev Workshop 2025 
# Funciones para integrar con LLMs via el SDK de Google y realizar consultas de texto.
import os
import json
import mimetypes
from google import genai
from google.genai import types
from config import Config


# Configuración Google
CFG_KEY = Config.LLM_GOOGLE_API_KEY
CFG_MOD = Config.LLM_GOOGLE_MODEL
CFG_MOD_IMG = Config.LLM_GOOGLE_MODEL_IMGE
CFG_TEM = Config.LLM_GOOGLE_TEMPERATURE
CFG_MAX = Config.LLM_GOOGLE_MAX_TOKENS


def get_client():
    """Se crea el cliente de Google"""
    client = genai.Client(api_key=CFG_KEY)
    return client


def invoke_by_text(client, text: str, model: str = CFG_MOD):

    if text is None or text.strip() == "":
        raise ValueError("El prompt está vacío")

    try:
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=text)],
            ),
        ]

        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=CFG_TEM,
                max_output_tokens=CFG_MAX,
                response_mime_type="application/json",   # <- IMPORTANTE
            ),
        )

        if not response or not response.text:
            raise ValueError("Respuesta vacía del modelo")

        txt_response = response.text.strip()

        # VALIDAR JSON REAL
        try:
            json.loads(txt_response)
        except Exception:
            raise ValueError("JSON incompleto generado por el modelo")

        llm_response = response.to_json_dict()

        return txt_response, llm_response

    except Exception as e:
        print(f"Error al invocar el SDK de Google: {e}")
        return None, None

def invoke_by_messages(client, messages: list, model: str = CFG_MOD):
    """Realiza una invocación a un LLM mediante el SDK de Google y retorna la respuesta como texto y como serializable."""
    try:
        contents = []
        for message in messages:
            role = message["role"]
            content = message["content"]
            contents.append(
                types.Content(role=role, parts=[types.Part.from_text(text=content)])
            )

        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=CFG_TEM,
                max_output_tokens=CFG_MAX,
            ),
        )

        txt_response = response.text
        llm_response = response.to_json_dict()

        return txt_response, llm_response
    except Exception as e:
        print(f"Error al invocar el SDK de Google: {e}")
        return None, None


def resolve_template(template, values):
    """Reemplaza variables en una plantilla de prompt con valores de un diccionario."""
    result = template
    for key, value in values.items():
        placeholder = "{" + key + "}"  # Creamos el marcador de posición como "{clave}"
        result = result.replace(placeholder, str(value))
    return result


def generate_image(client, text, directory, filename, model=CFG_MOD_IMG):
    """Genera una imagen a partir de un texto."""
    try:
        image_description = ""
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=text),
                ],
            ),
        ]
        config = types.GenerateContentConfig(
            response_modalities=[
                "IMAGE",
                "TEXT",
            ],
            response_mime_type="text/plain",
            temperature=CFG_TEM,
            max_output_tokens=CFG_MAX,
        )
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=config,
        ):
            if (
                chunk.candidates is None
                or chunk.candidates[0].content is None
                or chunk.candidates[0].content.parts is None
            ):
                continue
            if chunk.candidates[0].content.parts[0].inline_data:
                inline_data = chunk.candidates[0].content.parts[0].inline_data
                data_buffer = inline_data.data
                file_extension = mimetypes.guess_extension(inline_data.mime_type)
                full_filename = f"{filename}{file_extension}"
                _save_binary_file(directory, full_filename, data_buffer)
            else:
                image_description += chunk.text
        return full_filename, image_description
    except Exception as e:
        print(f"Error al invocar el SDK de Google: {e}")
        return None, None


def read_prompt_file(file):
    """Lee el contenido de un archivo de prompt."""
    file_path = os.path.join(Config.DIR_PROMPTS, file)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()


def clean_json(text) -> dict | None:
    """Limpia la respuesta de un LLM en JSON para convertirla en un diccionario de Python limpio."""
    if not text:
        return None

    # Eliminar 'json' si está al inicio
    text = text.replace("json", "").strip()

    # Eliminar backticks y la palabra json
    text = text.strip("`")

    # Eliminar marcadores de código de markdown
    text = text.replace("```json", "").replace("```", "")

    # Eliminar espacios y saltos de línea al inicio y final
    text = text.strip()

    try:
        # Parsear el texto como JSON
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Error al parsear JSON: {e}")
        print(f"Texto recibido: {text}")
        return None


def _save_binary_file(directory, file_name, data):
    full_file_name = os.path.join(directory, file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    f = open(full_file_name, "wb")
    f.write(data)
    f.close()


# Ejemplo de uso
if __name__ == "__main__":
    # Obtiene el cliente de Google
    cliente = get_client()

    # Ejemplo de uso de texto
    consulta = "Escribe un poema corto sobre un gato."
    respuesta, _ = invoke_by_text(cliente, consulta)
    print(f"Consulta: \n{consulta}\n")
    print(f"Respuesta de Google: \n{respuesta}\n\n")

    # Ejemplo de generación de imagen
    peticion = "Unos tacos al pastor."
    directorio = "imagenes"
    archivo = "tacos-al-pastor"
    archivo_final, descripcion_detallada = generate_image(
        cliente, peticion, directorio, archivo
    )
    print(f"Archivo generado: {archivo_final}\n")
    print(descripcion_detallada)