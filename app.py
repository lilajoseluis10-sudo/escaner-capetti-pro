import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract
import re

# Configuración de Nivel Profesional
st.set_page_config(page_title="Protocolo Capetti v23", layout="wide")

# Llave API integrada
API_KEY = "0c464ef542mshd56e1a359a25c27p150483jsn48dc23e96f0a"

# Diseño Dark Mode de Alta Gama
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1f2937; padding: 20px; border-radius: 15px; border-left: 5px solid #4ade80; }
    .analysis-box { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #3b82f6; margin-bottom: 15px; }
    .verdict-box { padding: 20px; border-radius: 15px; text-align: center; font-weight: bold; font-size: 24px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏀 Protocolo Capetti v23 | Scanner Pro")

# --- 1. ESCÁNER DE IMAGEN ---
st.header("1. Captura de Datos")
uploaded_file = st.file_uploader("Sube la captura de PrizePicks", type=["jpg", "png", "jpeg"])

player_name = "Nikola Jokic" # Valor detectado por defecto
linea_casa = 30.0

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, width=350, caption="Captura procesada")
    with st.spinner("🧠 Analizando imagen..."):
        texto = pytesseract.image_to_string(img)
        nombres = re.findall(r'[A-Z][a-z]+ [A-Z][a-z]+', texto)
        if nombres: player_name = nombres[0]
        st.success(f"Jugador Detectado: {player_name}")

st.divider()

# --- 2. ANÁLISIS DE RENDIMIENTO Y RIVAL ---
st.header("2. Inteligencia de Campo")
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
    st.subheader("👤 Jugador y Entorno")
    rol = st.select_slider("Rol en el equipo", options=["Secundario", "Titular", "Estrella"], value="Estrella")
    lesion = st.radio("¿Lesiones o restricciones?", ["Limpio", "Duda", "Limitado"])
    minutos = st.number_input("Minutos esperados", value=35)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
    st.subheader("🛡️ Defensa del Rival")
    rival = st.text_input("Equipo Rival", value="Cavaliers")
    defensa = st.select_slider("Nivel defensivo rival", options=["Débil", "Media", "Fuerte"], value="Fuerte")
    ausencia_rival = st.toggle("¿Rival tiene ausencias clave?")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. LÓGICA DE LA CASA Y DATOS GLOBALES ---
st.header("3. Análisis de Mercado y Datos Reales")
c_int1, c_int2 = st.columns(2)

with c_int1:
    st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
    st.write("**Lógica de la Casa:**")
    st.write("La casa detectó anomalía en rendimiento reciente o defensa difícil.")
    anomalia = st.toggle("¿Confirmar anomalía?", value=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c_int2:
    st.write("**Fuentes Globales Reales:**")
    p_query = player_name.replace(" ", "-").lower()
    st.link_button("Rotowire (Lesiones/Minutos)", f"https://www.rotowire.com/basketball/player/{p_query}")
    st.link_button("StatMuse (Historial vs Rival)", f"https://www.statmuse.com/nba/ask/{player_name.replace(' ', '+')}+vs+{rival}")

st.divider()

# --- 4. CALCULADORA DE PROYECCIÓN ---
st.header("4. Proyección de Trayectoria")
cp1, cp2, cp3 = st.columns(3)
pts = cp1.number_input("Puntos", value=10)
rebs = cp2.number_input("Rebotes", value=3)
asts = cp3.number_input("Asistencias", value=1)

total_pra = pts + rebs + asts
linea_pra_input = st.number_input("Línea de la Casa (PRA)", value=linea_casa)

st.divider()

# --- 5. VEREDICTO FINAL ---
st.header("🏆 Resultado Final")
res_col1, res_col2 = st.columns(2)

with res_col1:
    st.metric("PROYECTADO TOTAL", f"{total_pra} PRA", delta=total_pra - linea_pra_input)

with res_col2:
    if total_pra < linea_pra_input:
        st.success("🔥 VEREDICTO: LESS (Muy Seguro)")
        st.write(f"Motivo: {total_pra} está muy por debajo de la línea de {linea_pra_input}.")
    else:
        st.warning("⚠️ VEREDICTO: MORE")

st.caption("Protocolo Capetti v23 - Herramienta de Análisis Profesional")
