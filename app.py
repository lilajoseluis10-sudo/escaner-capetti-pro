import streamlit as st
import requests
import pytesseract
from PIL import Image
import re

# Configuración profesional y llave integrada
st.set_page_config(page_title="JLC-Scanner Pro", layout="wide")
API_KEY = "0c464ef542mshd56e1a359a25c27p150483jsn48dc23e96f0a"
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
}

st.title("🛡️ JLC-Scanner Pro | Automatización Total")
st.write("Sube la captura y el sistema hará el resto.")

# --- 1. CARGA Y ESCANEO ---
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, width=300)
    
    with st.spinner("🤖 Procesando imagen y consultando base de datos..."):
        # OCR: Extraer texto de la foto
        texto = pytesseract.image_to_string(img)
        
        # Detectar Nombre y Línea de la foto
        nombres = re.findall(r'[A-Z][a-z]+ [A-Z][a-z]+', texto)
        nombre_detectado = nombres[0] if nombres else "Desconocido"
        
        # Buscar línea PRA (ej: 26.5)
        pra_match = re.search(r"(\d+\.?\d*)", texto)
        linea_casa = float(pra_match.group(1)) if pra_match else 0.0

        # --- 2. CONEXIÓN AUTOMÁTICA CON API-NBA ---
        # Paso A: Buscar ID del jugador
        search_url = f"https://api-nba-v1.p.rapidapi.com/players?search={nombre_detectado.split()[-1]}"
        response = requests.get(search_url, headers=HEADERS).json()
        
        if response.get("response"):
            player_id = response["response"][0]["id"]
            
            # Paso B: Traer estadísticas de la temporada actual (2025-2026)
            stats_url = f"https://api-nba-v1.p.rapidapi.com/players/statistics?id={player_id}&season=2025"
            stats_data = requests.get(stats_url, headers=HEADERS).json()
            
            # Calcular promedios automáticos
            games = stats_data["response"]
            if games:
                pts = sum([int(g['points']) for g in games if g['points']]) / len(games)
                reb = sum([int(g['totReb']) for g in games if g['totReb']]) / len(games)
                ast = sum([int(g['assists']) for g in games if g['assists']]) / len(games)
                total_pra = pts + reb + ast
            else:
                total_pra = 0.0
        else:
            total_pra = 0.0

    # --- 3. RESULTADOS AUTOMÁTICOS ---
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 👤 {nombre_detectado}")
        st.metric("Línea en Foto", f"{linea_casa} PRA")
    
    with col2:
        st.markdown("### 📊 Proyección Real")
        st.metric("Promedio Temporada", f"{round(total_pra, 1)} PRA", delta=round(total_pra - linea_casa, 1))

    # --- 4. VEREDICTO ---
    if total_pra > 0:
        if total_pra < linea_casa:
            st.success(f"🎯 VEREDICTO: **LESS** (El promedio de {round(total_pra, 1)} está por debajo)")
        else:
            st.warning(f"🔥 VEREDICTO: **MORE** (El promedio de {round(total_pra, 1)} supera la línea)")
    else:
        st.error("No se pudieron obtener estadísticas automáticas para este jugador.")
else:
    st.info("Esperando captura de PrizePicks para iniciar el análisis automático.")
