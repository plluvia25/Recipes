# apoyo_app1.py - GenAI Dev Workshop 2025 by alfredo.de.regil
# Funciones de apoyo para la aplicación de recetas
import os
from datetime import datetime
import pandas as pd
import streamlit as st
import apoyo_llm_google_sdk as llm_google
import apoyo_llm_groq_sdk as llm_groq
import apoyo_archivos as archivos
from config import Config
CFG_FMT_FEC = Config.FMT_FECHAS


# Configuraciones usadas

@st.cache_resource
def obtiene_cliente_groq():
    """Obtiene y almacena en caché la instancia del cliente de Groq."""
    return llm_groq.get_client()


@st.cache_resource
def obtiene_cliente_google():
    """Obtiene y almacena en caché la instancia del modelo de Google."""
    return llm_google.get_client()


# Funciones de apoyo para cargar y guardar recetas
##########################################################################################


def carga_recetas():
    """Obtiene la lista ordenada de archivos JSON de recetas existentes."""
    recetas = archivos.lee_directorio()
    return recetas


def guarda_receta(receta):
    """Almacena la receta en un archivo JSON con nombre basado en timestamp."""

    # Crear nombre de archivo
    archivo = receta["archivo"] + ".json"

    # Guarda el archivo
    archivos.escribe_archivo(receta, archivo)


def carga_receta_guardada(nombre_archivo):
    """Carga una receta guardada desde un archivo JSON. Espera el nombre del archivo sin la ruta."""
    receta = archivos.lee_archivo(nombre_archivo)
    return receta


# Manejadores para widgets de la interfaz - al terminar, generan un rerun
##########################################################################################


def formatea_nombre_receta(nombre_archivo):
    """Convierte nombre de archivo de receta a formato legible para mostrar."""
    # Quitar timestamp y extensión
    nombre_sin_fecha = nombre_archivo[12:-5]
    # Convertir guiones a espacios y capitalizar
    nombre_formateado = nombre_sin_fecha.replace("-", " ").title()
     # Capitalize properly (English title case)
    palabras_excluidas = {"and", "or", "the", "of", "in", "on", "with", "a", "an"}
    
    palabras = nombre_formateado.split()
    titulo = []
    
    for i, palabra in enumerate(palabras):
        if i == 0 or palabra not in palabras_excluidas:
            titulo.append(palabra.capitalize())
        else:
            titulo.append(palabra.lower())
    
    return " ".join(titulo)


def maneja_carga_receta():
    """Carga la receta seleccionada en el estado de la sesión."""
    nombre_archivo = st.session_state.widget_select_box_receta_seleccionada

    receta = carga_receta_guardada(nombre_archivo)

    # Actualiza receta actual
    st.session_state.receta_actual = receta

    # Actualiza el área de texto de ingredientes
    iniciales_str = ", ".join(receta["iniciales"])
    st.session_state.widget_text_area_ingredientes = iniciales_str


def maneja_genera_receta():
    """Genera una nueva receta basada en los ingredientes ingresados."""
    ingredientes = st.session_state.widget_text_area_ingredientes
    if ingredientes:
        with st.spinner("Generating recipe ...", show_time=True):

            # Función de apoyo para llamadas a LLMs para generar la nueva receta
            nueva_receta = genera_receta_llm(ingredientes)

            if nueva_receta:
                # Actualiza receta actual
                st.session_state.receta_actual = nueva_receta

                # Almacena la receta en un archivo JSON
                guarda_receta(nueva_receta)


def maneja_limpia_receta_actual():
    """Limpia la receta actual del estado de la sesión."""
    st.session_state.receta_actual = None
    st.session_state.widget_select_box_receta_seleccionada = None
    st.session_state.widget_text_area_ingredientes = None


# Funciones para desplegar información de la receta y demás
##########################################################################################


def muestra_info_receta(receta):
    """Muestra los componentes de una receta en formato HTML compacto."""
    # CSS personalizado para reducir el espacio vertical
    st.markdown(
        """
        <style>
        .compact-list {
            margin-bottom: 1em;
        }
        .compact-list ul, .compact-list ol {
            margin: 0;
            padding-left: 0px;
        }
        .compact-list li {
            margin-bottom: 0;
            line-height: 1;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Mostrar ingredientes usando ul/li
    st.write("🥗 **Ingredients**")
    with st.container():
        ingredientes_html = "<div class='compact-list'><ul>"
        for ingrediente in receta["ingredientes"]:
            ingredientes_html += f"<li>{ingrediente}</li>"
        ingredientes_html += "</ul></div>"
        st.markdown(ingredientes_html, unsafe_allow_html=True)

    # Mostrar instrucciones usando ol/li
    st.write("📋 **Instructions**")
    with st.container():
        instrucciones_html = "<div class='compact-list'><ol>"
        for instruccion in receta["instrucciones"]:
            instrucciones_html += f"<li>{instruccion}</li>"
        instrucciones_html += "</ol></div>"
        st.markdown(instrucciones_html, unsafe_allow_html=True)

    # Mostrar notas usando ul/li si existen
    if receta["notas"]:
        st.write("📌**Grades**")
        with st.container():
            notas_html = "<div class='compact-list'><ul>"
            for nota in receta["notas"]:
                notas_html += f"<li>{nota}</li>"
            notas_html += "</ul></div>"
            st.markdown(notas_html, unsafe_allow_html=True)


def muestra_info_nutricional(receta):
    """Muestra métricas y gráfica comparativa de información nutricional."""
    # Sección de información nutricional
    st.write("📊 **Nutritional Information**")
    datos = receta["nutricional"]
    st.metric("Calories", f"{datos['calorias']} kcal", border=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Proteins", f"{datos['proteinas']} g", border=True)
    col2.metric("Carbohydrates", f"{datos['carbohidratos']} g", border=True)
    col3.metric("Fats", f"{datos['grasas']} g", border=True)


def muestra_info_comparativo(receta):
    """Muestra comparativo de calorías de todas las recetas."""
    recetas_guardadas = carga_recetas()
    if recetas_guardadas:
        calorias_recetas = []
        for nombre_archivo in recetas_guardadas:
            receta = carga_receta_guardada(nombre_archivo)
            nombre_receta = receta["nombre"]
            calorias = receta["nutricional"]["calorias"]
            calorias_recetas.append({"Recipe": nombre_receta, "Calories": calorias})

        # Crear DataFrame y ordenarlo por calorías
        df_calorias = pd.DataFrame(calorias_recetas)
        df_calorias = df_calorias.sort_values("Calories", ascending=True)

        # Establecer el índice como los nombres de las recetas
        df_calorias = df_calorias.set_index("Recipe")

        # Mostrar gráfica comparativa usando bar_chart
        with st.container(border=True):
            st.write("🔥 **Calories Across Recipes**")
            st.bar_chart(df_calorias, horizontal=True, width="stretch")


def muestra_info_footer(receta):
    mensaje = f"| **Provider:** {receta['proveedor']} | **Creation:** {receta['fecha']} | **Ingredients:** {', '.join(receta['iniciales'])} "
    st.caption(mensaje)

    # Funciones de apoyo
##########################################################################################





# Funciones de apoyo
##########################################################################################


def genera_nombre_archivo(nombre, fecha):
    """Genera un nombre de archivo para una nueva receta. Se usa para json y para imágenes. No incluye extensión."""

    # Limpia el nombre de receta para usarlo como parte del nombre  del archivo
    nombre = nombre.lower()
    nombre_limpio = ""
    for caracter in nombre:
        if caracter.isalnum():
            nombre_limpio += caracter
        else:
            nombre_limpio += "-"

    # Eliminar guiones múltiples
    while "--" in nombre_limpio:
        nombre_limpio = nombre_limpio.replace("--", "-")

    # Crear nombre de archivo
    archivo = f"{fecha}-{nombre_limpio}"

    return archivo


# Llamada a LLM para generar receta y obtener información nutricional
##########################################################################################


def genera_receta_llm(ingredientes):
    """Crea una nueva receta y su información nutricional usando LLMs."""
    proveedor = st.session_state.widget_radio_proveedor

    # Decide el LLM y funciones a llamar
    if proveedor == "Groq":
        cliente = obtiene_cliente_groq()
        llm_read_prompt_file = llm_groq.read_prompt_file
        llm_resolve_template = llm_groq.resolve_template
        llm_invoke_by_text = llm_groq.invoke_by_text
        llm_clean_json = llm_groq.clean_json

    elif proveedor == "Google":
        cliente = obtiene_cliente_google()
        llm_read_prompt_file = llm_google.read_prompt_file
        llm_resolve_template = llm_google.resolve_template
        llm_invoke_by_text = llm_google.invoke_by_text
        llm_clean_json = llm_google.clean_json
    else:
        st.error(f"Proveedor '{proveedor}' no identificado.")
        return None

    lista_ingredientes = [
        ingrediente.strip() for ingrediente in ingredientes.split(",")
    ]

    # Paso 1: Crear receta
    plantilla = llm_read_prompt_file("p1-receta.txt")
    valores = {"ingredientes": lista_ingredientes}
    prompt = llm_resolve_template(plantilla, valores)
    txt_response, _ = llm_invoke_by_text(cliente, prompt)
    receta = llm_clean_json(txt_response)

    if not receta:
        st.error("Error generating the recipe. Please try again.")
        return None

    # Paso 2: Calcular información nutricional
    plantilla = llm_read_prompt_file("p2-nutricion.txt")
    ingredientes_medidos = "\n".join(receta["ingredientes"])
    valores = {"ingredientes_medidos": ingredientes_medidos}
    prompt = llm_resolve_template(plantilla, valores)
    txt_response, _ = llm_invoke_by_text(cliente, prompt)
    nutricion = llm_clean_json(txt_response)

    if not nutricion:
        st.error(
            "Error calculating nutritional information. Please try again."
        )
        return None

    # Genera nombre del archivo de la receta
    nombre = receta["nombre"]
    fecha = datetime.now().strftime(CFG_FMT_FEC)
    archivo = genera_nombre_archivo(nombre, fecha)

    # Paso final, construye la estructura completa
    estructura_receta = {
        "nombre": nombre,
        "fecha": fecha,
        "archivo": archivo,
        "proveedor": proveedor,
        "iniciales": lista_ingredientes,
        "ingredientes": receta["ingredientes"],
        "instrucciones": receta["instrucciones"],
        "notas": receta["notas"],
        "nutricional": nutricion,
    }

    return estructura_receta