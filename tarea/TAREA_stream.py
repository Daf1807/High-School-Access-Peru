#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import os
import folium
from streamlit.components.v1 import html

# Configuración inicial
st.set_page_config(layout="wide", page_title="Análisis de Colegios por Distrito")

st.title("📊 Análisis Espacial de Colegios por Nivel Educativo")
st.markdown("Este dashboard interactivo permite visualizar la distribución de colegios por nivel en diferentes distritos.")

# -------------------------------
# Carga de datos
# -------------------------------

@st.cache_data
def cargar_datos():
    final_df = pd.read_excel('archivo_final.xlsx')
    maps = gpd.read_file(r"C:\Users\usuario\Documents\GitHub\High-School-Access-Peru\shape_file\DISTRITOS.shp")
    
    if 'UBIGEO' not in maps.columns:
        maps['UBIGEO'] = maps['IDDPTO'].astype(str).str.zfill(2) + \
                         maps['IDPROV'].astype(str).str.zfill(2) + \
                         maps['IDDIST'].astype(str).str.zfill(2)

    maps['UBIGEO'] = maps['UBIGEO'].astype(int)
    maps = maps[['UBIGEO', 'geometry']]
    
    return final_df, maps

final_df, maps = cargar_datos()

# -------------------------------
# Clasificar nivel
# -------------------------------

def clasificar_nivel(nivel):
    if isinstance(nivel, str):
        nivel = nivel.lower()
        if 'inicial' in nivel:
            return 'Inicial'
        elif 'primaria' in nivel:
            return 'Primaria'
        elif 'secundaria' in nivel:
            return 'Secundaria'
    return None

final_df['Nivel_Simple'] = final_df['Nivel / Modalidad'].apply(clasificar_nivel)
final_df['Ubigeo'] = final_df['Ubigeo'].astype(int)

# -------------------------------
# Sidebar
# -------------------------------

nivel = st.sidebar.selectbox("Selecciona el nivel educativo", ['Inicial', 'Primaria', 'Secundaria'])
colormap = {'Inicial': 'Oranges', 'Primaria': 'Blues', 'Secundaria': 'Greens'}

# -------------------------------
# Conteo por distrito
# -------------------------------

conteo_df = final_df[final_df['Nivel_Simple'] == nivel].groupby('Distrito').size().reset_index(name='Cantidad')
conteo_df = conteo_df.merge(final_df[['Distrito', 'Ubigeo']].drop_duplicates(), on='Distrito', how='left')
map_df = maps.merge(conteo_df, left_on='UBIGEO', right_on='Ubigeo', how='left')
map_df['Cantidad'] = map_df['Cantidad'].fillna(0)

# -------------------------------
# Mapa de distribución
# -------------------------------

with st.expander("🗂️ Tab 1: Data Description"):
    st.markdown("### Descripción de la unidad de análisis")
    st.markdown("Los datos provienen de un archivo Excel que contiene información sobre colegios en Perú. Cada fila representa un colegio, con columnas que incluyen el nombre de la institución, el nivel educativo, la latitud y longitud de su ubicación, y la provincia a la que pertenece.")
    st.markdown("### Fuentes de datos")
    st.markdown("Los datos fueron proporcionados por la base de datos del Ministerio de Educación del Perú (MINEDU) y fuentes geográficas como los distritos de Perú.")
    st.markdown("### Supuestos y Preprocesamiento")
    st.markdown("Se han realizado algunos preprocesamientos, como la clasificación del nivel educativo basado en la columna 'Nivel / Modalidad' y la asignación de coordenadas geográficas para la representación espacial.")

with st.expander("🗺️ Tab 2: Static Maps"):
    
    # Imágenes estáticas
    st.image(r'C:\Users\usuario\Documents\GitHub\High-School-Access-Peru\tarea\mapa_inicial.png', caption='Mapa Inicial')
    st.image(r'C:\Users\usuario\Documents\GitHub\High-School-Access-Peru\tarea\mapa_primaria.png', caption='Mapa Primaria')
    st.image(r'C:\Users\usuario\Documents\GitHub\High-School-Access-Peru\tarea\mapa_secundaria.png', caption='Mapa Secundaria')
    

with st.expander("🌍 Tab 3: Dynamic Maps"):
    # Cargar los mapas dinámicos de Folium
    st.markdown("#### Mapa Interactivo: Huancavelica")
    map_file = r'C:\Users\usuario\Documents\GitHub\High-School-Access-Peru\tarea\mapa_proximidad_Huancavelica.html'
    with open(map_file, 'r', encoding='utf-8') as f:
        folium_map = f.read()
    html(folium_map, width=700, height=500)

    st.markdown("#### Mapa Interactivo: Huanuco")
    map_file = r'C:\Users\usuario\Documents\GitHub\High-School-Access-Peru\tarea\mapa_proximidad_Huanuco.html'
    with open(map_file, 'r', encoding='utf-8') as f:
        folium_map = f.read()
    html(folium_map, width=700, height=500)

# -------------------------------
# Final
# -------------------------------

st.success("✅ Análisis completado.")




# In[4]:


#!jupyter nbconvert --to script TAREA_stream.ipynb

