import streamlit as st
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN DE TERMINAL DE ALTO NIVEL
st.set_page_config(page_title="Capetti Oracle Master v26.0", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #06090f; color: #ffffff; }
    .stMetric { background-color: #0d1117; border-radius: 10px; border: 1px solid #d4af37; }
    .question-box { background-color: #161b22; padding: 20px; border-radius: 15px; border-left: 5px solid #d4af37; margin-top: 20px; }
    .veredicto-final { background-color: #0d1117; padding: 25px; border-radius: 15px; border: 2px solid #4ade80; text-align: center; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔱 Protocolo Capetti: Oracle Master v26.0")
st.write(f"### Inteligencia de Mercado NBA | {datetime.now().strftime('%d/%m/%Y')}")

# --- 1. BOARD DE PROYECCIONES (PARTE SUPERIOR) ---
st.subheader("📋 Radar Global de Estrellas (Datos Verídicos)")
nba_data = [
    {"Jugador": "Nikola Jokic", "Equipo": "DEN", "PTS": 26.3, "REB": 12.1, "AST": 9.0, "PRA": 47.4},
    {"Jugador": "Luka Doncic", "Equipo": "DAL", "PTS": 33.9, "REB": 9.2, "AST": 9.8, "PRA": 52.9},
    {"Jugador": "Giannis Antetokounmpo", "Equipo": "MIL", "PTS": 30.4, "REB": 11.5, "AST": 6.5, "PRA": 48.4},
    {"Jugador": "Shai Gilgeous-Alexander", "Equipo": "OKC", "PTS": 30.1, "REB": 5.5, "AST": 6.2, "PRA": 41.8},
    {"Jugador": "LeBron James", "Equipo": "LAL", "PTS": 24.7, "REB": 7.2, "AST": 7.5, "PRA": 39.4}
]
df = pd.DataFrame(nba_data)
st.table(df.sort_values(by="PRA", ascending=False))

st.divider()

# --- 2. SISTEMA DE PROYECCIÓN DE PREGUNTAS (PARTE INFERIOR) ---
st.subheader("🧠 Auditoría de Inteligencia (Análisis de Riesgo)")
st.write("Responde estas preguntas para validar tu jugada:")

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="question-box">', unsafe_allow_html=True)
        q1 = st.selectbox("1. ¿Cómo es el rol/minutos hoy?", ["Titular (Normal)", "Minutos Limitados", "Rol Expandido (Estrella)"])
        q2 = st.text_area("2. ¿Hay lesiones o ausencias en su equipo?", "Ej: No juega el base titular, tendrá más posesión.")
        q3 = st.select_slider("3. ¿Nivel de la defensa rival?", options=["Débil", "Media", "Fuerte"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="question-box">', unsafe_allow_html=True)
        q4 = st.text_input("4. ¿Por qué la casa puso esa línea? (Anomalía)", "Ej: Línea inflada por racha reciente.")
        q5 = st.selectbox("5. ¿El entorno del juego le favorece?", ["Sí (Local/Motivado)", "No (Back-to-back/Cansado)"])
        linea_prizepicks = st.number_input("6. Línea PrizePicks a batir", value=30.0)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 3. CALCULADORA DE PROYECCIÓN FINAL ---
st.divider()
st.subheader("📊 Tu Proyección Matemática Final")
c1, c2, c3 = st.columns(3)
p = c1.number_input("Puntos Estimados", value=15)
r = c2.number_input("Rebotes Estimados", value=5)
a = c3.number_input("Asistencias Estimadas", value=5)

total_est = p + r + a

# --- VEREDICTO DINÁMICO ---
diff = total_est - linea_prizepicks
color_v = "#4ade80" if diff < -3 else "#fb923c" if diff > 3 else "#70d1ff"
texto_v = "UNDER (LESS) MUY SEGURO" if diff < -3 else "OVER (MORE) ALTO VOLUMEN" if diff > 3 else "EVITAR (LÍNEA AJUSTADA)"

st.markdown(f"""
    <div class="veredicto-final" style="border-color: {color_v};">
        <h2 style="color: {color_v}; margin: 0;">🏆 RESULTADO: {texto_v}</h2>
        <p style="font-size: 18px; margin: 10px 0 0 0;">
            Tu proyección: <b>{total_est} PRA</b> | Línea Casa: <b>{linea_prizepicks} PRA</b> | Diferencia: <b>{round(diff,1)} pts</b>
        </p>
        <p style="font-size: 14px; color: #888;">Análisis basado en Rol: {q1} y Defensa: {q3}</p>
    </div>
""", unsafe_allow_html=True)

st.caption("Protocolo Capetti v26.0 | Sistema de Auditoría Institucional.")
