#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import base64
from PIL import Image
import io
import os
import streamlit.components.v1 as components

# Configuración de página
st.set_page_config(
    page_title="Análisis de Colegios - Huancavelica y Ayacucho",
    page_icon="🏫",
    layout="wide"
)

# Función para mostrar imágenes reales (no placeholders)
def display_image(image_path):
    try:
        # Cargar la imagen real desde el sistema de archivos
        image = Image.open(image_path)
        st.image(image, caption=f"Mapa: {os.path.basename(image_path)}", use_container_width=True)
    except Exception as e:
        st.error(f"Error al cargar la imagen {image_path}: {e}")
        st.write(f"Asegúrate de que la imagen exista en la ruta: {image_path}")

# Función para cargar HTML local (para mapas dinámicos)
def display_html_file(html_path):
    try:
        # Leer el contenido del archivo HTML
        with open(html_path, 'r', encoding='utf-8') as f:
            html_data = f.read()
        
        # Mostrar el HTML utilizando el componente de HTML de Streamlit
        components.html(html_data, height=600, scrolling=True)
        
    except FileNotFoundError:
        st.error(f"No se encontró el archivo HTML: {html_path}")
        st.write(f"Por favor, verifica que el archivo existe en la ruta: {html_path}")
        
        # Crear un mapa folium básico como respaldo
        st.write("Mostrando un mapa de respaldo:")
        m = folium.Map(location=[-13.0456, -74.2178], zoom_start=8)
        folium.Marker(
            [-13.0456, -74.2178], 
            popup="Ejemplo de mapa dinámico", 
            tooltip="Punto central"
        ).add_to(m)
        folium_static(m)
    except Exception as e:
        st.error(f"Error al cargar el HTML: {e}")

# Función para crear tabla informativa
def create_info_table(data_dict):
    df = pd.DataFrame(list(data_dict.items()), columns=['Nivel Educativo', 'Total'])
    return df

# Datos para las tablas
huancavelica_data = {
    "Inicial": 1836,
    "Primaria": 1598,
    "Secundaria": 442
}

ayacucho_data = {
    "Inicial": 2300,
    "Primaria": 1518,
    "Secundaria": 563
}

total_combined_data = {
    "Inicial": 4136,
    "Primaria": 3116,
    "Secundaria": 1005
}

# APLICACIÓN PRINCIPAL
st.title("🏫 Análisis de Instituciones Educativas")
st.subheader("Huancavelica y Ayacucho - Perú")

# Crear pestañas
tab1, tab2, tab3 = st.tabs(["🗂️ Descripción de Datos", "🗺️ Mapas Estáticos", "🌍 Mapas Dinámicos"])

# PESTAÑA 1: DESCRIPCIÓN DE DATOS
with tab1:
    st.header("Descripción de Datos")
    
    # Unidad de análisis
    st.subheader("Unidad de Análisis")
    st.write("""
    Este análisis examina la distribución de instituciones educativas en los departamentos 
    de Huancavelica y Ayacucho, considerando los niveles educativos de Inicial, Primaria y Secundaria.
    """)
    
    # Tablas informativas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Total Combinado")
        st.table(create_info_table(total_combined_data))
    
    with col2:
        st.subheader("Huancavelica")
        st.table(create_info_table(huancavelica_data))
    
    with col3:
        st.subheader("Ayacucho")
        st.table(create_info_table(ayacucho_data))
    
    # Fuentes de datos
    st.subheader("Fuentes de Datos")
    st.write("""
    El conjunto de datos proporcionado contiene información detallada sobre diversas instituciones 
    educativas. Incluye datos como el código único de cada institución, su nombre, ubicación geográfica 
    (latitud, longitud y altitud), el nivel educativo que ofrecen, su modalidad (pública o privada) y 
    la dependencia administrativa. También se detalla la dirección física de las instituciones, 
    el código del centro poblado cercano y la fuente de las coordenadas geográficas utilizadas para su localización.
    
    Estos datos son útiles para la gestión educativa y análisis geográfico. Se realizó un merge entre los datos 
    de las instituciones educativas y un archivo de formas (shapefile) para poder elaborar los mapas estáticos 
    y dinámicos que se presentan en este análisis.
    """)

# PESTAÑA 2: MAPAS ESTÁTICOS
with tab2:
    st.header("Mapas Estáticos")
    
    # División para Huancavelica y Ayacucho
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Huancavelica")
        
        # Mapas estáticos de Huancavelica - Usando rutas absolutas correctas
        huancavelica_maps = [
            "C:/Users/usuario/Documents/GitHub/High-School-Access-Peru/tarea/Huancavelica_inicial.png",
            "C:/Users/usuario/Documents/GitHub/High-School-Access-Peru/tarea/Huancavelica_primaria.png",
            "C:/Users/usuario/Documents/GitHub/High-School-Access-Peru/tarea/Huancavelica_secundaria.png"
        ]
        
        for map_path in huancavelica_maps:
            level_name = os.path.basename(map_path).split('_')[-1].split('.')[0].capitalize()
            st.write(f"**{level_name}**")
            display_image(map_path)
    
    with col2:
        st.subheader("Ayacucho")
        
        # Mapas estáticos de Ayacucho - Usando rutas absolutas correctas
        ayacucho_maps = [
            "C:/Users/usuario/Documents/GitHub/High-School-Access-Peru/tarea/ayacucho_inicial.png",
            "C:/Users/usuario/Documents/GitHub/High-School-Access-Peru/tarea/ayacucho_primaria.png",
            "C:/Users/usuario/Documents/GitHub/High-School-Access-Peru/tarea/ayacucho_secundaria.png"
        ]
        
        for map_path in ayacucho_maps:
            level_name = os.path.basename(map_path).split('_')[-1].split('.')[0].capitalize()
            st.write(f"**{level_name}**")
            display_image(map_path)

# PESTAÑA 3: MAPAS DINÁMICOS
with tab3:
    st.header("Mapas Dinámicos")
    
    # Mapa dinámico de proximidad para Huancavelica
    st.subheader("Mapa de Proximidad - Huancavelica")
    
    html_path = "C:/Users/usuario/Documents/GitHub/High-School-Access-Peru/tarea/mapa_proximidad_huancavelica.html"
    display_html_file(html_path)
    
    st.write("""
    Este mapa interactivo muestra la distribución espacial de las instituciones educativas en Huancavelica, 
    permitiendo analizar la proximidad entre centros educativos y áreas pobladas.
    
    Para navegar por el mapa:
    - Utiliza el zoom para acercarte o alejarte
    - Haz clic sobre los marcadores para ver información detallada
    - Puedes arrastrar el mapa para explorar diferentes áreas
    """)

# Agregar una sección para reportar problemas
st.sidebar.header("Información de Depuración")
st.sidebar.write("Si encuentras problemas con los mapas:")
st.sidebar.write("1. Verifica que las rutas de los archivos sean correctas")
st.sidebar.write("2. Asegúrate de que los archivos existan en las ubicaciones especificadas")
st.sidebar.write("3. Revisa los permisos de acceso a los archivos")

# Mostrar las rutas actuales para facilitar la depuración
if st.sidebar.checkbox("Mostrar rutas de archivos"):
    st.sidebar.subheader("Rutas de mapas estáticos:")
    for path in huancavelica_maps + ayacucho_maps:
        st.sidebar.code(path)
    st.sidebar.subheader("Ruta de mapa dinámico:")
    st.sidebar.code(html_path)

