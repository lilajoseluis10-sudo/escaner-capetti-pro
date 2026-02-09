import streamlit as st
import requests
import pandas as pd
import time

# --- CONFIGURACIÓN DE PODER JLC-SCANER ---
API_KEY = "0c464ef542mshd56e1a359a25c27p150483jsn48dc23e96f0a"
HOST = "api-nba-v1.p.rapidapi.com"

st.set_page_config(page_title="JLC-Scaner Pro", page_icon="🏀", layout="wide")

# Inicialización de Memoria Permanente
if 'huella' not in st.session_state: st.session_state.huella = []
if 'stats' not in st.session_state: st.session_state.stats = {"W": 0, "L": 0}

# --- ESTÉTICA PROFESIONAL ---
st.markdown("""
    <style>
        .stApp { background-color: #050505; color: #ffffff; }
        .card { background: #111; border-radius: 15px; padding: 20px; border: 1px solid #333; margin-bottom: 10px; }
        .pilar-box { background: #1a1a1a; padding: 15px; border-radius: 10px; text-align: center; border-bottom: 3px solid #00ff7f; }
        .veredicto-over { color: #00ff7f; font-size: 2.5rem; font-weight: bold; text-align: center; }
        .veredicto-under { color: #ff4b4b; font-size: 2.5rem; font-weight: bold; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🏀 JLC-SCANER ELITE V26</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00ff7f;'>CONEXIÓN REAL NBA DATA - FEBRERO 2026</p>", unsafe_allow_html=True)

# --- PANEL DE RÉCORD ---
c1, c2, c3 = st.columns(3)
c1.metric("GANADAS (W)", st.session_state.stats["W"])
c2.metric("DERROTAS (L)", st.session_state.stats["L"])
total = st.session_state.stats["W"] + st.session_state.stats["L"]
efec = (st.session_state.stats["W"]/total*100) if total > 0 else 0
c3.metric("EFECTIVIDAD", f"{efec:.1f}%")

st.divider()

# --- ENTRADA DE DATOS REALES ---
with st.container():
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        jugador_nombre = st.text_input("👤 NOMBRE DEL JUGADOR (Ejem: LeBron James)")
        foto = st.file_uploader("📥 INYECTAR CAPTURA PRIZEPICKS", type=["jpg", "png", "jpeg"])
    with col_in2:
        linea_casa = st.number_input("🎯 LÍNEA DE LA CASA (PRA)", value=15.5, step=0.5)
        if st.button("🚀 EJECUTAR PREDICCIÓN REAL"):
            if jugador_nombre:
                with st.spinner(f'🧬 CONSULTANDO SERVIDORES NBA PARA {jugador_nombre.upper()}...'):
                    # --- LLAMADA REAL A LA API ---
                    url = f"https://{HOST}/players/statistics"
                    querystring = {"season": "2025", "search": jugador_nombre} # Temporada actual 2025-26
                    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}
                    
                    try:
                        response = requests.get(url, headers=headers, params=querystring)
                        data = response.json()
                        
                        if data['response']:
                            # Procesamiento de los últimos partidos
                            recent_stats = data['response'][-5:] # Últimos 5 juegos
                            avg_pts = sum([int(i['points']) for i in recent_stats]) / 5
                            avg_reb = sum([int(i['rebounds']) for i in recent_stats]) / 5
                            avg_ast = sum([int(i['assists']) for i in recent_stats]) / 5
                            pra_real = avg_pts + avg_reb + avg_ast
                            
                            # Predicción basada en datos reales
                            es_over = (pra_real * 0.55) > (linea_casa * 0.5) # Ajuste para 1ra Mitad
                            
                            nuevo_analisis = {
                                "id": time.time(),
                                "nombre": jugador_nombre,
                                "proy": round(pra_real * 0.55, 1),
                                "linea": linea_casa,
                                "veredicto": "MÁS (OVER)" if es_over else "MENOS (UNDER)",
                                "pilares": [round(avg_pts,1), round(avg_reb,1), round(avg_ast,1)]
                            }
                            st.session_state.huella.insert(0, nuevo_analisis)
                            st.success("¡Análisis Real Completado!")
                        else:
                            st.error("No se encontró al jugador. Revisa el nombre.")
                    except:
                        st.error("Error de conexión con la API.")
            else:
                st.warning("Escribe el nombre del jugador para buscar sus datos reales.")

st.divider()

# --- LA HUELLA: LISTA PERMANENTE DE AUDITORÍA ---
st.subheader("📋 Tu Lista Maestra de Verdad")
for idx, p in enumerate(st.session_state.huella):
    with st.container():
        color_v = "veredicto-over" if p['veredicto'] == "MÁS (OVER)" else "veredicto-under"
        st.markdown(f"""
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="font-size:1.5rem;">{p['nombre']}</b>
                    <span class="{color_v}">{p['veredicto']}</span>
                </div>
                <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; margin-top:15px;">
                    <div class="pilar-box"><small>AVG PTS</small><br><b>{p['pilares'][0]}</b></div>
                    <div class="pilar-box"><small>AVG REB</small><br><b>{p['pilares'][1]}</b></div>
                    <div class="pilar-box"><small>AVG AST</small><br><b>{p['pilares'][2]}</b></div>
                </div>
                <p style="margin-top:15px; color:#aaa;">Línea Casa: {p['linea']} | Proyección Real 1H: <b>{p['proy']}</b></p>
            </div>
        """, unsafe_allow_html=True)
        
        c_btn1, c_btn2, c_btn3, c_btn4 = st.columns([1,1,1,3])
        if c_btn1.button("✅ GANÓ", key=f"w_{p['id']}"):
            st.session_state.stats["W"] += 1
            st.rerun()
        if c_btn2.button("❌ PERDIÓ", key=f"l_{p['id']}"):
            st.session_state.stats["L"] += 1
            st.rerun()
        if c_btn3.button("🗑️ BORRAR", key=f"d_{p['id']}"):
            st.session_state.huella.pop(idx)
            st.rerun()
