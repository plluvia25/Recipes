# apoyo_llm_groq_sdk.py - GenAI Dev Workshop 2025 
# Funciones para integrar con LLMVs via el SDK de Groq y realizar consultas de texto.
import os
import json
from groq import Groq
from config import Config


# Configuración Groq
CFG_KEY = Config.LLM_GROQ_API_KEY
CFG_MOD = Config.LLM_GROQ_MODEL
CFG_TEM = Config.LLM_GROQ_TEMPERATURE
CFG_MAX = Config.LLM_GROQ_MAX_TOKENS


def get_client():
    """Se crea el cliente de Groq"""
    client = Groq(api_key=CFG_KEY)
    return client


def invoke_by_text(client, text, model: str = CFG_MOD):
    """Realiza una invocación a un LLM mediante el SDK de Groq y retorna la respuesta como texto y como serializable."""
    try:
        user_message = {"role": "user", "content": text}
        messages = [user_message]
        chat_completion = client.chat.completions.create(
            messages=messages, model=model, temperature=CFG_TEM, max_tokens=CFG_MAX
        )

        response = chat_completion.choices[0].message.content

        txt_response = response
        llm_response = chat_completion.to_dict()

        return txt_response, llm_response
    except Exception as e:
        print(f"Error al invocar el SDK de Groq: {e}")
        return None, None


def invoke_by_messages(client, messages: list, model: str = CFG_MOD):
    """Realiza una invocación a un LLM mediante el SDK de Groq y retorna la respuesta como texto y como serializable."""
    try:
        chat_completion = client.chat.completions.create(
            messages=messages, model=model, temperature=CFG_TEM, max_tokens=CFG_MAX
        )

        response = chat_completion.choices[0].message.content

        txt_response = response
        llm_response = chat_completion.to_dict()

        return txt_response, llm_response
    except Exception as e:
        print(f"Error al invocar el SDK de Groq: {e}")
        return None, None


def resolve_template(template, values):
    """Reemplaza variables en una plantilla de prompt con valores de un diccionario."""
    result = template
    for key, value in values.items():
        placeholder = "{" + key + "}"  # Creamos el marcador de posición como "{clave}"
        result = result.replace(placeholder, str(value))
    return result


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


# Ejemplo de uso
if __name__ == "__main__":
    consulta = "Escribe un poema corto sobre un gato."
    client = get_client()
    respuesta, _ = invoke_by_text(client, consulta)
    print(f"Consulta: \n{consulta}\n")
    print(f"Respuesta de Groq: \n{respuesta}\n")