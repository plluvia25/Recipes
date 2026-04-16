import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # GOOGLE
    LLM_GOOGLE_API_KEY = os.getenv("LLM_GOOGLE_API_KEY")
    LLM_GOOGLE_MODEL = os.getenv("LLM_GOOGLE_MODEL")
    LLM_GOOGLE_MODEL_IMGE = os.getenv("LLM_GOOGLE_MODEL_IMGE")
    LLM_GOOGLE_TEMPERATURE = float(os.getenv("LLM_GOOGLE_TEMPERATURE", "0.2"))
    LLM_GOOGLE_MAX_TOKENS = int(os.getenv("LLM_GOOGLE_MAX_TOKENS", "2048"))

    # GROQ
    LLM_GROQ_API_KEY = os.getenv("LLM_GROQ_API_KEY")
    LLM_GROQ_MODEL = os.getenv("LLM_GROQ_MODEL")
    LLM_GROQ_TEMPERATURE = float(os.getenv("LLM_GROQ_TEMPERATURE", "0.2"))
    LLM_GROQ_MAX_TOKENS = int(os.getenv("LLM_GROQ_MAX_TOKENS", "2048"))
    
    # Rutas
    DIR_ARCHIVOS = os.getenv("DIR_ARCHIVOS", "archivos")
    DIR_IMAGENES = os.getenv("DIR_IMAGENES", "imagenes")

    # Formatos
    FMT_FECHAS = os.getenv("FMT_FECHAS", "%Y-%m-%d")
    DIR_PROMPTS = os.getenv("DIR_PROMPTS", "prompts")


# Variables obligatorias
Config_vars_required = [
    "LLM_GOOGLE_API_KEY",
    "LLM_GROQ_API_KEY"
]

for var in Config_vars_required:
    if getattr(Config, var) is None:
        raise ValueError(f"Falta la variable {var} en el archivo .env")