import streamlit as st
import requests
import pytesseract
from PIL import Image
import re
import time

# --- CONFIGURACIÓN ÉLITE JLC-SCANER ---
API_KEY = "0c464ef542mshd56e1a359a25c27p150483jsn48dc23e96f0a"
HOST = "api-nba-v1.p.rapidapi.com"

st.set_page_config(page_title="JLC-Scaner Pro", page_icon="🏀", layout="wide")

if 'lista' not in st.session_state: st.session_state.lista = []
if 'stats' not in st.session_state: st.session_state.stats = {"W": 0, "L": 0}

st.markdown("""
    <style>
        .stApp { background-color: #050505; color: #ffffff; }
        .card { background: #111; border-radius: 15px; padding: 20px; border: 1px solid #333; margin-bottom: 10px; }
        .veredicto { font-size: 2rem; font-weight: bold; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🏀 JLC-SCANER ELITE: MOTOR REAL")

# --- PANEL DE CONTROL ---
c1, c2, c3 = st.columns(3)
c1.metric("GANADAS", st.session_state.stats["W"])
c2.metric("DERROTAS", st.session_state.stats["L"])
total = st.session_state.stats["W"] + st.session_state.stats["L"]
efec = (st.session_state.stats["W"]/total*100) if total > 0 else 0
c3.metric("EFECTIVIDAD", f"{efec:.1f}%")

st.divider()

# --- ESCÁNER AUTOMÁTICO ---
foto = st.file_uploader("📥 INYECTAR CAPTURA DE PRIZEPICKS", type=["jpg", "png", "jpeg"])

if foto:
    with st.spinner('🧠 LEYENDO IMAGEN Y CONSULTANDO API REAL 2026...'):
        img = Image.open(foto)
        texto = pytesseract.image_to_string(img)
        
        # Lógica para encontrar nombres y líneas en la foto
        # (Buscamos patrones comunes en PrizePicks)
        linea_match = re.search(r"(\d+\.?\d?)", texto)
        linea_detectada = float(linea_match.group(1)) if linea_match else 15.5
        
        # Extraemos el primer nombre que parezca un jugador (simplificado)
        nombres_comunes = ["LeBron", "Curry", "Tatum", "Butler", "Doncic", "Embiid", "Giannis", "Durant"]
        jugador_final = "Jugador"
        for n in nombres_comunes:
            if n.lower() in texto.lower():
                jugador_final = n
                break

        # LLAMADA REAL A LA NBA
        url = f"https://{HOST}/players/statistics"
        querystring = {"season": "2025", "search": jugador_final if jugador_final != "Jugador" else "James"}
        headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}
        
        try:
            res = requests.get(url, headers=headers, params=querystring).json()
            if res['response']:
                stats = res['response'][-5:]
                avg_pra = (sum([int(s['points']) for s in stats]) + 
                           sum([int(s['rebounds']) for s in stats]) + 
                           sum([int(s['assists']) for s in stats])) / 5
                
                proy_1h = round(avg_pra * 0.55, 1)
                es_over = proy_1h > linea_detectada
                
                nuevo = {
                    "id": time.time(),
                    "nombre": jugador_final,
                    "proy": proy_1h,
                    "linea": linea_detectada,
                    "vered": "MÁS (OVER)" if es_over else "MENOS (UNDER)",
                    "pts": round(sum([int(s['points']) for s in stats])/5, 1)
                }
                st.session_state.lista.insert(0, nuevo)
                st.success(f"Detección exitosa: {jugador_final} | Línea: {linea_detectada}")
        except:
            st.error("Error en conexión real.")

# --- LISTA DE AUDITORÍA PERMANENTE ---
st.subheader("📋 Tu Lista de Verdad")
for idx, p in enumerate(st.session_state.lista):
    color = "#00ff7f" if "MÁS" in p['vered'] else "#ff4b4b"
    st.markdown(f"""
        <div class="card" style="border-left: 5px solid {color};">
            <div style="display:flex; justify-content:space-between;">
                <b>{p['nombre']}</b>
                <span style="color:{color}; font-weight:bold;">{p['vered']}</span>
            </div>
            <p>Proyección Real 1H: {p['proy']} | Línea: {p['linea']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_b1, col_b2, col_b3 = st.columns([1,1,4])
    if col_b1.button("✅ GANÓ", key=f"w_{p['id']}"):
        st.session_state.stats["W"] += 1
        st.rerun()
    if col_b2.button("❌ PERDIÓ", key=f"l_{p['id']}"):
        st.session_state.stats["L"] += 1
        st.rerun()
    if col_b3.button("🗑️ BORRAR", key=f"d_{p['id']}"):
        st.session_state.lista.pop(idx)
        st.rerun()
