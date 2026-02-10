import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract
import requests

# Configuración profesional de la página
st.set_page_config(page_title="JLC-Scanner Pro", page_icon="🏀", layout="wide")

# Estilo personalizado (Dark Mode Elegante)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #3b82f6; }
    div[data-testid="stExpander"] { border: 1px solid #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# Encabezado
st.title("🏀 JLC-Scanner Pro")
st.subheader("Análisis de Apuestas en Tiempo Real")

# --- SECCIÓN DE MÉTRICAS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="VICTORIAS", value="0", delta="0%")
with col2:
    st.metric(label="DERROTAS", value="0", delta="0%", delta_color="inverse")
with col3:
    st.metric(label="EFECTIVIDAD", value="0.0%", delta="Listo")

st.divider()

# --- SIDEBAR (CONFIGURACIÓN) ---
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("NBA API Key", type="password", help="Pega aquí tu llave de API-NBA")
    st.info("El escáner usará OCR para leer PrizePicks.")

# --- CARGA DE CAPTURA ---
st.markdown("### 📥 Inyectar Captura de PrizePicks")
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Mostrar vista previa
    img = Image.open(uploaded_file)
    st.image(img, caption="Imagen cargada correctamente", width=400)
    
    with st.spinner("🧠 Escaneando datos con Inteligencia Artificial..."):
        try:
            # Lógica de OCR
            texto_extraido = pytesseract.image_to_string(img)
            
            # --- DISEÑO DE RESULTADOS ---
            st.success("✅ Escaneo completado")
            
            expander = st.expander("Ver Datos Extraídos")
            expander.write(texto_extraido)
            
            # Aquí se conectará con el API-NBA en el siguiente paso
            st.warning("⚠️ Conectando con API-NBA para validar cuotas...")
            
        except Exception as e:
            st.error(f"Error en el procesador: {str(e)}")
else:
    st.info("Esperando captura para iniciar el análisis...")

# Pie de página
st.markdown("---")
st.caption("JLC-Scanner Pro v2.0 - Desarrollado para análisis profesional")
