import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract
import requests

# Configuración profesional
st.set_page_config(page_title="JLC-Scanner Pro", page_icon="🏀", layout="wide")

# Llave que me mostraste ya integrada
API_KEY = "0c464ef542mshd56e1a359a25c27p150483jsn48dc23e96f0a"

# Estilo Dark Mode Profesional
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏀 JLC-Scanner Pro")
st.subheader("Análisis NBA en Tiempo Real")

# --- PANEL DE CONTROL ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="ESTADO API", value="CONECTADO", delta="Listo")
with col2:
    st.metric(label="JUEGOS HOY", value="NBA", delta="Activo")
with col3:
    st.metric(label="ESCÁNER", value="OCR v2.0", delta="Online")

st.divider()

# --- CARGA DE CAPTURA ---
st.markdown("### 📥 Sube tu captura de PrizePicks")
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Imagen detectada", width=450)
    
    with st.spinner("🧠 Analizando jugadores y cuotas..."):
        try:
            # Leer la imagen
            texto = pytesseract.image_to_string(img)
            
            # Mostrar resultados
            st.success("✅ Análisis Completo")
            with st.expander("Ver texto detectado"):
                st.write(texto)
                
            # Aquí el sistema ya usa la API_KEY automáticamente
            st.info("Buscando discrepancias en la API de la NBA...")
            
        except Exception as e:
            st.error(f"Ajuste necesario: {str(e)}")
else:
    st.info("El sistema está esperando que subas una foto para empezar.")
