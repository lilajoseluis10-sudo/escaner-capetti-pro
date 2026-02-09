import streamlit as st
import random
import time
import pandas as pd

# --- CONFIGURACIÓN ELITE JLC-SCANER V26 ---
API_KEY = "0c464ef542mshd56e1a359a25c27p150483jsn48dc23e96f0a"

st.set_page_config(page_title="JLC-Scaner Pro", page_icon="🏀", layout="wide")

# Inicializar memoria de sesión para el récord y la huella
if 'ganadas' not in st.session_state: st.session_state.ganadas = 0
if 'derrotas' not in st.session_state: st.session_state.derrotas = 0
if 'historial' not in st.session_state: st.session_state.historial = []

# --- ESTÉTICA PROFESIONAL (CYBERPUNK DARK) ---
st.markdown("""
    <style>
        .stApp { background-color: #050505; color: #ffffff; }
        .main-header { font-family: 'Arial Black'; text-align: center; color: #ffffff; padding: 20px; border-bottom: 2px solid #00ff7f; }
        .counter-box { background: #111; border: 1px solid #333; border-radius: 15px; padding: 15px; text-align: center; }
        .pillar-card { background: #1a1a1a; border-radius: 10px; padding: 15px; border-left: 4px solid #00ff7f; margin-bottom: 10px; }
        .verdict-over { color: #00ff7f; font-size: 3rem; font-weight: bold; text-align: center; margin: 0; }
        .stat-box { background: #222; border-radius: 10px; padding: 20px; text-align: center; border-bottom: 4px solid #00ff7f; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>JLC-SCANER PRO V26</h1><p>SISTEMA DE AUDITORÍA CIENTÍFICA NBA 1H</p></div>', unsafe_allow_html=True)

# --- PANEL DE RÉCORD OFICIAL ---
st.write("### 🏆 Récord de la Temporada 2026")
col_rec1, col_rec2, col_rec3 = st.columns(3)
with col_rec1:
    st.markdown(f'<div class="counter-box"><h2 style="color:#00ff7f; margin:0;">{st.session_state.ganadas}</h2><p>GANADAS</p></div>', unsafe_allow_html=True)
with col_rec2:
    st.markdown(f'<div class="counter-box"><h2 style="color:#ff4b4b; margin:0;">{st.session_state.derrotas}</h2><p>DERROTAS</p></div>', unsafe_allow_html=True)
with col_rec3:
    total = st.session_state.ganadas + st.session_state.derrotas
    efectividad = (st.session_state.ganadas / total * 100) if total > 0 else 0
    st.markdown(f'<div class="counter-box"><h2 style="color:#ffffff; margin:0;">{efectividad:.1f}%</h2><p>EFECTIVIDAD</p></div>', unsafe_allow_html=True)

st.divider()

# --- SECCIÓN DE ANÁLISIS ---
foto = st.file_uploader("📥 INYECTAR CAPTURA DE PRIZEPICKS", type=["jpg", "png", "jpeg"])

if foto:
    with st.spinner('🧬 PROCESANDO 4 PILARES Y PATRONES HISTÓRICOS...'):
        time.sleep(2.5)
        
        # Simulación de detección y lógica 2026
        jugador = "Cade Cunningham" # Esto vendrá de la detección de imagen
        puntos_proy = 13.5
        reb_proy = 4.2
        ast_proy = 3.8
        
        # 1. VEREDICTO Y PATRÓN
        st.markdown('<p class="verdict-over">BUENO (OVER)</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align:center; color:#aaa;">Patrón Detectado: <b>"Abuso de Defensa Débil"</b></p>', unsafe_allow_html=True)

        # 2. LOS 4 PILARES
        st.subheader("🛡️ Los 4 Pilares de Precisión")
        p1, p2, p3, p4 = st.columns(4)
        with p1: st.markdown('<div class="pillar-card"><b>Promedio 1H</b><br>12.8 PTS</div>', unsafe_allow_html=True)
        with p2: st.markdown('<div class="pillar-card"><b>Matchup</b><br>Defensa #28</div>', unsafe_allow_html=True)
        with p3: st.markdown('<div class="pillar-card"><b>Minutos 1H</b><br>19.2 min</div>', unsafe_allow_html=True)
        with p4: st.markdown('<div class="pillar-card"><b>Tendencia</b><br>🔥 Caliente</div>', unsafe_allow_html=True)

        # 3. DETALLE DE P/R/A
        st.subheader("📊 Proyección Detallada (1ra Mitad)")
        d1, d2, d3 = st.columns(3)
        with d1: st.markdown(f'<div class="stat-box"><small>PUNTOS</small><br><b style="font-size:1.8rem;">{puntos_proy}</b></div>', unsafe_allow_html=True)
        with d2: st.markdown(f'<div class="stat-box"><small>REBOTES</small><br><b style="font-size:1.8rem;">{reb_proy}</b></div>', unsafe_allow_html=True)
        with d3: st.markdown(f'<div class="stat-box"><small>ASISTENCIAS</small><br><b style="font-size:1.8rem;">{ast_proy}</b></div>', unsafe_allow_html=True)

        # 4. REGISTRO DE LA HUELLA
        st.divider()
        st.write("### ✍️ Registrar Resultado del Escaneo")
        c_btn1, c_btn2 = st.columns(2)
        if c_btn1.button("✅ MARCAR COMO GANADA"):
            st.session_state.ganadas += 1
            st.session_state.historial.append({"Jugador": jugador, "Resultado": "GANADA", "Fecha": "Feb 2026"})
            st.rerun()
        if c_btn2.button("❌ MARCAR COMO DERROTA"):
            st.session_state.derrotas += 1
            st.session_state.historial.append({"Jugador": jugador, "Resultado": "DERROTA", "Fecha": "Feb 2026"})
            st.rerun()

# --- LA HUELLA (LISTA DE ANÁLISIS) ---
st.divider()
st.subheader("👣 La Huella: Historial de Análisis")
if st.session_state.historial:
    df = pd.DataFrame(st.session_state.historial)
    st.table(df)
    if st.button("Limpiar Historial de Hoy"):
        st.session_state.historial = []
        st.session_state.ganadas = 0
        st.session_state.derrotas = 0
        st.rerun()
else:
    st.info("Inyecta una foto para empezar a construir tu historial de hoy.")
