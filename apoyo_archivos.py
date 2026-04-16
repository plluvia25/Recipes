# apoyo_archivos.py - GenAI Dev Workshop 2025 por alfredo.de.regil
# Funciones para acceder y manipular archivos de datos
import os, json
from datetime import datetime
from config import Config

# Configuración
DIR_ARCHIVOS = Config.DIR_ARCHIVOS
FMT_FECHAS = Config.FMT_FECHAS

def lee_directorio():
    """Devuelve una lista ordenada de los nombres de archivo sin la ruta."""
    if not os.path.exists(DIR_ARCHIVOS):
        return []

    listado = os.listdir(DIR_ARCHIVOS)
    archivos = [f for f in listado if f.endswith(".json")]
    archivos.sort(reverse=False)
    return archivos


def lee_archivo(archivo):
    """Carga datos desde un archivo JSON. Se espera el nombre del archivo sin la ruta."""
    ruta_archivo = _ruta_completa(archivo)
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            return json.load(f)


def elimina_archivo(archivo):
    """Elimina un archivo."""
    ruta_archivo = _ruta_completa(archivo)
    if os.path.exists(ruta_archivo):
        os.remove(ruta_archivo)


def escribe_archivo(datos, archivo=None):
    """Guarda datos en un archivo JSON. Devuelve el nombre del archivo sin la ruta."""
    if not os.path.exists(DIR_ARCHIVOS):
        os.makedirs(DIR_ARCHIVOS)
    if not archivo:
        timestamp = datetime.now().strftime(FMT_FECHAS)
        archivo = f"{timestamp}.json"
    ruta_archivo = _ruta_completa(archivo)
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False, sort_keys=False)
    return archivo


def actualiza_archivo(archivo, datos):
    """Actualiza datos en un archivo JSON existente."""
    ruta_archivo = _ruta_completa(archivo)
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)


def _ruta_completa(archivo):
    """Construye la ruta completa para un archivo JSON de datos."""
    return os.path.join(DIR_ARCHIVOS, archivo)