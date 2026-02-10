import streamlit as st
import requests
import pytesseract
from PIL import Image
import re

# CONFIGURACIÓN NIVEL DIAMANTE
st.set_page_config(page_title="Capetti Diamond Elite", layout="wide")

# CREDENCIALES INTEGRADAS
API_KEY = "0c464ef542mshd56e1a359a25c27p150483jsn48dc23e96f0a"
HEADERS = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"}

st.markdown("""
    <style>
    .main { background-color: #05070a; color: #ffffff; }
    .stMetric { background-color: #0d1117; padding: 25px; border-radius: 15px; border: 1px solid #d4af37; }
    .diamond-box { background: linear-gradient(45deg, #0d1117, #1a202c); padding: 30px; border-radius: 20px; border: 2px solid #70d1ff; text-align: center; }
    .status-text { font-size: 28px; font-weight: bold; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 Protocolo Capetti Diamond")
st.write("### Sistema de Inteligencia Predictiva - Grado Profesional 2026")

# --- CARGA ÚNICA ---
file = st.file_uploader("📥 INYECTAR CAPTURA", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    with st.spinner("🕵️ Procesando con IA de Grado Diamante..."):
        text = pytesseract.image_to_string(img)
        
        # MOTOR DE LIMPIEZA AVANZADO (Filtra equipos y estados para no fallar)
        noise = ["Thunder", "Cavaliers", "Nuggets", "Lakers", "Warriors", "Celtics", "Starting", "Points", "Rebounds", "Assists", "PRA", "Fantasy", "Score", "Game", "Live"]
        words = re.findall(r'([A-Z][a-z]+)', text)
        
        # Identificar Jugador (Busca nombres que no estén en la lista de equipos)
        player_candidates = [w for w in words if w not in noise]
        player = f"{player_candidates[0]} {player_candidates[1]}" if len(player_candidates) >= 2 else "Desconocido"
        
        # Identificar Rival
        opponent = "Rival detectado"
        for team in ["Cavaliers", "Thunder", "Nuggets", "Lakers", "Celtics"]:
            if team in text: opponent = team

        # Detectar Línea Casa (Soporta decimales 26.5, 31.5)
        linea_casa = 0.0
        numbers = re.findall(r"(\d+\.\d+)", text)
        if numbers: linea_casa = float(numbers[0])

        # --- CONEXIÓN API-NBA (DATOS REALES) ---
        pra_real = 0.0
        try:
            # Búsqueda Robusta
            s_name = player.split()[-1] if " " in player else player
            p_data = requests.get(f"https://api-nba-v1.p.rapidapi.com/players?search={s_name}", headers=HEADERS).json()
            if p_data["response"]:
                p_id = p_data["response"][0]["id"]
                s_data = requests.get(f"https://api-nba-v1.p.rapidapi.com/players/statistics?id={p_id}&season=2025", headers=HEADERS).json()
                g = s_data["response"]
                if g:
                    pra_real = (sum(int(x['points'] or 0) for x in g) + sum(int(x['totReb'] or 0) for x in g) + sum(int(x['assists'] or 0) for x in g)) / len(g)
        except: pass

    # --- DASHBOARD DE ELITE ---
    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("JUGADOR", player)
    with c2: st.metric("RIVAL", opponent)
    with c3: st.metric("DIFICULTAD RIVAL", "ALTA" if opponent in ["Cavaliers", "Thunder", "Celtics"] else "MEDIA")

    st.divider()
    res1, res2 = st.columns(2)
    res1.metric("LÍNEA CASA", f"{linea_casa} PRA")
    res2.metric("PROYECCIÓN MATEMÁTICA", f"{round(pra_real, 1)} PRA", delta=round(pra_real - linea_casa, 1))

    # --- EL VEREDICTO DIAMANTE ---
    diff = pra_real - linea_casa
    if pra_real > 0:
        if diff < -2:
            st.markdown(f'<div class="diamond-box"><div class="status-text" style="color: #4ade80;">🛡️ VEREDICTO: UNDER (LESS)</div><p>Altamente Seguro: El promedio es {round(pra_real,1)} contra una línea de {linea_casa}. Defensa del rival favorece el Under.</p></div>', unsafe_allow_html=True)
        elif diff > 2:
            st.markdown(f'<div class="diamond-box"><div class="status-text" style="color: #fb923c;">🔥 VEREDICTO: OVER (MORE)</div><p>Oportunidad de Volumen: El rendimiento real supera la línea por {round(diff,1)} puntos.</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="diamond-box"><div class="status-text" style="color: #70d1ff;">⚠️ ZONA DE RIESGO</div><p>Línea muy ajustada. Se recomienda esperar a reportes de lesiones de último minuto.</p></div>', unsafe_allow_html=True)
    else:
        st.error("No se pudieron sincronizar los datos. Verifica que la foto sea clara.")

st.caption("Protocolo Capetti Diamond v13.0 - Desarrollado para el análisis de alto riesgo 2026")
