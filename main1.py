# main.py - GenAI Dev Workshop 2025 
# 06-Recetas - Generador de recetas con ingredientes
import streamlit as st
import apoyo_app1 as app


def main():
    """Implementa la interfaz principal de usuario para la aplicación Recipes."""

    # Configura página y pone título
    st.set_page_config(layout="wide", page_icon="🧑‍🍳", page_title="Recipes AI")
    st.title("🧑‍🍳 RECIPES AI")

    # Inicializa objetos de sesión si no existen
    if "receta_actual" not in st.session_state:
        st.session_state.receta_actual = None

    # Configura el diseño de la página
    contenedor_lateral = st.sidebar
    contenedor_contenido = st.container()

    # LAYOUT: BARRA LATERAL
    # ########################################################################################
    with contenedor_lateral:

        # Sección de recetas guardadas
        st.header("📚Saved Recipes")
        recetas = app.carga_recetas()
        if recetas:
            st.selectbox(
                "Select a recipe.:",
                recetas,
                format_func=app.formatea_nombre_receta,
                key="widget_select_box_receta_seleccionada",
                on_change=app.maneja_carga_receta,
            )

        # Sección de nueva receta
        st.header("📝 New Recipe")
        st.text_area(
            "Ingredients (separated by commas):",
            "",
            key="widget_text_area_ingredientes",
            height=70,
        )

        st.radio(
            "Select the provider:",
            ["Google", "Groq"],
            key="widget_radio_proveedor",
            horizontal=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            st.button(
                "Generar",
                use_container_width=True,
                type="primary",
                on_click=app.maneja_genera_receta,
            )
        with col2:
            st.button(
                "Limpiar",
                use_container_width=True,
                on_click=app.maneja_limpia_receta_actual,
            )
        st.info("Experiment with different ingredients and observe the results.")

        # Separador
        st.divider()

        # Sección de acerca de la aplicación
        with st.expander("ℹ️ About the Application"):
            st.markdown(
                """
                Application to demonstrate:

                - Aplicación web Streamlit
                - Plantillas de prompts
                - LLMs via SDK proveedores                
                - Generación de imágenes
                - Guarda recetas en JSON

                ---
                --📝 GenAI Dev Workshop 2025  
                🔖 v1.0.0
                """
            )

    # LAYOUT: CONTENIDO PRINCIPAL
    # ########################################################################################
    with contenedor_contenido:
        receta = st.session_state.receta_actual
        if receta:
            with st.container(border=True):
                st.header(receta["nombre"])
                col1, col2 = st.columns(2)
                with col1:
                    app.muestra_info_receta(receta)
                with col2:
                    app.muestra_info_nutricional(receta)
                    app.muestra_info_comparativo(receta)

            app.muestra_info_footer(receta)


# Punto de entrada de la aplicación
if __name__ == "__main__":
    main()