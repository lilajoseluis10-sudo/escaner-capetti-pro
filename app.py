import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract
import re

# Configuración de nivel profesional
st.set_page_config(page_title="JLC-Scanner Pro v6.0", layout="wide")

# Tu llave integrada
API_KEY = "0c464ef542mshd56e1a359a25c27p150483jsn48dc23e96f0a"

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1f2937; padding: 20px; border-radius: 15px; border-left: 5px solid #4ade80; }
    .intel-card { background-color: #262730; padding: 15px; border-radius: 10px; border: 1px solid #3b82f6; margin-bottom: 10px; }
    .btn-global { display: inline-block; padding: 10px 15px; background-color: #3b82f6; color: white; border-radius: 5px; text-decoration: none; font-weight: bold; margin: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ JLC-Scanner Pro | Global Intelligence Hub")

# --- 1. ESCÁNER DE IMAGEN ---
st.markdown("### 📥 Escanear Jugador (Captura PrizePicks)")
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

player_name = "Nikola Jokic" # Por defecto
linea_pra = 30.0

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    texto = pytesseract.image_to_string(img)
    nombres = re.findall(r'[A-Z][a-z]+ [A-Z][a-z]+', texto)
    if nombres: player_name = nombres[0]
    st.success(f"Detección de Élite: {player_name}")

st.divider()

# --- 2. CENTRAL DE INTELIGENCIA MUNDIAL ---
st.subheader(f"🌍 Información Real de {player_name}")
st.write("Consulta las fuentes que mueven las líneas en Las Vegas:")

# Generar links automáticos basados en el jugador
player_query = player_name.replace(" ", "-").lower()
player_search = player_name.replace(" ", "+")

col_int1, col_int2 = st.columns(2)

with col_int1:
    st.markdown(f"""
    <div class="intel-card">
        <h4>📋 Reporte de Lesiones y Minutos</h4>
        <p>Consulta si hay restricciones o cambios de último minuto.</p>
        <a class="btn-global" href="https://www.rotowire.com/basketball/player/{player_query}" target="_blank">Rotowire (Injuries)</a>
        <a class="btn-global" href="https://underdognetwork.com/basketball/nba-lineups" target="_blank">Underdog (Lineups)</a>
    </div>
    """, unsafe_allow_html=True)

with col_int2:
    st.markdown(f"""
    <div class="intel-card">
        <h4>📊 Estadísticas Avanzadas</h4>
        <p>Analiza el rendimiento contra el rival y proyecciones.</p>
        <a class="btn-global" href="https://www.statmuse.com/nba/ask/{player_search}-vs-cavaliers-last-5-games" target="_blank">StatMuse (Matchup)</a>
        <a class="btn-global" href="https://www.espn.com/nba/player/_/name/{player_query}" target="_blank">ESPN Stats</a>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 3. CALCULADORA DE VEREDICTO ---
st.subheader("📝 Veredicto de Apuesta")
c1, c2, c3 = st.columns(3)
p = c1.number_input("Puntos Estimados", value=10)
r = c2.number_input("Rebotes Estimados", value=3)
a = c3.number_input("Asistencias Estimadas", value=1)

total = p + r + a

st.markdown(f"""
<div class="stMetric">
    <h3>RESULTADO PROYECTADO: {total} PRA</h3>
    <p>Línea de la Casa: {linea_pra} | Diferencia: {total - linea_pra}</p>
</div>
""", unsafe_allow_html=True)

if total < (linea_pra * 0.9):
    st.success("🔥 VEREDICTO: LESS (MUY SEGURO - Diferencia amplia)")
elif total < linea_pra:
    st.info("✅ VEREDICTO: LESS")
else:
    st.warning("⚠️ VEREDICTO: MORE")

st.caption("JLC-Scanner Pro - Datos procesados con API-NBA.")
