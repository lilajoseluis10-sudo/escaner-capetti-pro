import streamlit as st
import requests
import pytesseract
from PIL import Image
import re

# CONFIGURACIÓN DE ALTA GAMA
st.set_page_config(page_title="Protocolo Capetti Gold", layout="wide")

# LLAVE MAESTRA
API_KEY = "0c464ef542mshd56e1a359a25c27p150483jsn48dc23e96f0a"
HEADERS = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"}

# ESTILO "PROFESSIONAL TRADER" (Inspirado en Thinkorswim)
st.markdown("""
    <style>
    .main { background-color: #0a0e14; color: #e0e0e0; }
    .stMetric { background-color: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .status-box { padding: 20px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 22px; margin-top: 10px; }
    .gold-text { color: #d4af37; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔱 Protocolo Capetti Gold")
st.write("### Terminal de Inteligencia NBA v12.0")

# --- 1. MOTOR DE DETECCIÓN BLINDADO ---
file = st.file_uploader("📥 INYECTAR CAPTURA DE PRIZEPICKS", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    with st.spinner("🧠 Ejecutando Algoritmo de Limpieza..."):
        raw_text = pytesseract.image_to_string(img)
        
        # Diccionario de Limpieza para evitar errores como "Thunder Starting"
        nba_teams = ["Thunder", "Lakers", "Celtics", "Cavaliers", "Nuggets", "Warriors", "Bulls", "Knicks", "Starting", "Game", "Fantasy", "Score", "Points"]
        
        # Extraer nombres (Palabra Mayúscula + Palabra Mayúscula)
        possible_names = re.findall(r'([A-Z][a-z]+ [A-Z][a-z]+)', raw_text)
        player = "Desconocido"
        for name in possible_names:
            if not any(team in name for team in nba_teams):
                player = name
                break
        
        # Detectar línea PRA (ej: 26.5)
        linea_match = re.search(r"(\d+\.?\d*)", raw_text)
        linea_casa = float(linea_match.group(1)) if linea_match else 0.0

    # --- 2. CÁLCULO ESTADÍSTICO MATEMÁTICO ---
    pra_real = 0.0
    try:
        # Buscamos al jugador en la API oficial
        search_name = player.split()[-1] if " " in player else player
        p_res = requests.get(f"https://api-nba-v1.p.rapidapi.com/players?search={search_name}", headers=HEADERS).json()
        
        if p_res["response"]:
            p_id = p_res["response"][0]["id"]
            # Consultamos temporada 2025/2026
            s_res = requests.get(f"https://api-nba-v1.p.rapidapi.com/players/statistics?id={p_id}&season=2025", headers=HEADERS).json()
            games = s_res["response"]
            if games:
                pts = sum(int(g['points'] or 0) for g in games) / len(games)
                reb = sum(int(g['totReb'] or 0) for g in games) / len(games)
                ast = sum(int(g['assists'] or 0) for g in games) / len(games)
                # Fórmula Matemática: $PRA = PTS + REB + AST$
                pra_real = pts + reb + ast
    except Exception: pass

    # --- 3. DASHBOARD DE RESULTADOS ---
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**JUGADOR**")
        st.markdown(f"<span class='gold-text'>{player}</span>", unsafe_allow_html=True)
        st.write(f"Rival detectado en foto.")

    with col2:
        st.metric("LÍNEA CASA", f"{linea_casa} PRA")
    
    with col3:
        diff = round(pra_real - linea_casa, 1)
        st.metric("PROYECCIÓN API", f"{round(pra_real, 1)} PRA", delta=diff)

    # --- 4. VEREDICTO DE PROBABILIDAD ---
    st.divider()
    if pra_real > 0:
        if pra_real < linea_casa:
            st.markdown(f'<div class="status-box" style="background-color: #064e3b; color: #34d399;">🟢 VEREDICTO: UNDER (LESS) <br> <span style="font-size: 14px;">El promedio histórico es {round(pra_real,1)}, muy por debajo de {linea_casa}.</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-box" style="background-color: #7c2d12; color: #fb923c;">🔥 VEREDICTO: OVER (MORE) <br> <span style="font-size: 14px;">El jugador está rindiendo por encima de la línea proyectada.</span></div>', unsafe_allow_html=True)
    else:
        st.error("Error de Sincronización: El motor no pudo verificar los datos. Reintenta con otra captura.")

    # Enlace a profundidad
    st.markdown(f"---")
    st.markdown(f"🔎 [Analizar entorno y lesiones de {player}](https://www.statmuse.com/nba/ask/{player.replace(' ', '+')}+stats+this+season)")

else:
    st.info("Sube una captura para activar el Protocolo Capetti Gold.")
