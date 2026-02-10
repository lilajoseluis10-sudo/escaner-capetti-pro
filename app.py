import streamlit as st
import pandas as pd
import requests
import pytesseract
import cv2
import numpy as np
from PIL import Image
import shutil

# --- CONFIGURACIÓN DE TESSERACT PARA LA NUBE ---
tesseract_path = shutil.which("tesseract")
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="José Líder - Capetti Pro Scanner", layout="wide")
st.title("🚀 Capetti Pro Scanner")
st.subheader("Análisis de NBA y Tenis - Protocolo Capetti")

# --- VARIABLES ---
API_KEY = "75315ae5e6153c3f9e3800bbc9814b7ae88313bdc9f6dcb289bf30a27fe20892"

# --- FUNCIONES DE PROCESAMIENTO ---
def scan_prizepicks_image(uploaded_file):
    """Procesa la imagen para extraer nombres y líneas."""
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # OCR para leer el texto
    text = pytesseract.image_to_string(gray)
    return text

def get_odds_data(sport_key):
    """Obtiene datos de la API de Odds."""
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?apiKey={API_KEY}&regions=us&markets=h2h,totals"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al conectar con la API de Odds.")
        return []

# --- INTERFAZ DE USUARIO ---
tab1, tab2 = st.tabs(["🎾 Tenis (1st Set)", "🏀 NBA (PRA/1H)"])

with tab1:
    st.header("Escáner de Tenis")
    uploaded_tennis = st.file_uploader("Sube captura de PrizePicks (Tenis)", type=['png', 'jpg', 'jpeg'], key="tennis")
    
    if uploaded_tennis:
        with st.spinner("Escaneando imagen..."):
            extracted_text = scan_prizepicks_image(uploaded_tennis)
            st.success("Texto extraído con éxito")
            # Aquí iría la lógica de comparación que definimos antes
            st.write(extracted_text)

with tab2:
    st.header("Escáner NBA")
    uploaded_nba = st.file_uploader("Sube captura de PrizePicks (NBA)", type=['png', 'jpg', 'jpeg'], key="nba")
    
    if st.button("Actualizar Probabilidades NBA"):
        data = get_odds_data("basketball_nba")
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)

# --- PIE DE PÁGINA ---
st.sidebar.markdown("---")
st.sidebar.write("👤 **Usuario:** José Líder")
st.sidebar.info("Recuerda que para que el OCR funcione en la nube, debes tener el archivo 'packages.txt' configurado.")
