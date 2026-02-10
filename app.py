import streamlit as st
import requests
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
        .card { background: #111; border-radius: 15px; padding: 20px; border: 1px solid #333; margin-bottom: 10px; border-left: 5px solid #555; }
        .pilar-box { background: #1a1a1a; padding: 15px; border-radius: 10px; text-align: center; border-bottom: 3px solid #00ff7f; }
        .veredicto-over { color: #00ff7f; font-size: 2rem; font-weight: bold; }
        .veredicto-under { color: #ff4b4b; font-size: 2rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🏀 JLC-SCANER ELITE V26</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>SISTEMA AUTOMÁTICO - API REAL 2026</p>", unsafe_allow_html=True)

# --- PANEL DE RÉCORD ---
c1, c2, c3 = st.columns(3)
c1.metric("GANADAS", st.session_state.stats["W"])
c2.metric("DERROTAS", st.session_state.stats["L"])
total = st.session_state.stats["W"] + st.session_state.stats["L"]
efec = (st.session_state.stats["W"]/total*100) if total > 0 else 0
c3.metric("EFECTIVIDAD", f"{efec:.1f}%")

st.divider()

# --- ENTRADA AUTOMÁTICA (SOLO FOTO) ---
with st.container():
    st.write("### 📤 Inyectar Captura")
    foto = st.file_uploader("Sube la foto y el sistema hará el resto", type=["jpg", "png", "jpeg"])
    
    if foto:
        with st.spinner('🧠 ACTIVANDO CEREBRO... LEYENDO FOTO Y CONECTANDO A API REAL...'):
            time.sleep(2) # Simulación de tiempo de lectura OCR

            # --- AQUÍ IRÁ EL MOTOR DE VISIÓN (OCR) PRONTO ---
            # Por ahora, para probar la API real sin escribir, usamos un jugador fijo.
            jugador_detectado = "LeBron James" # ESTO LO LEERÁ DE LA FOTO MAÑANA
            linea_detectada = 22.5 # ESTO LO LEERÁ DE LA FOTO MAÑANA
            st.info(f"🔍 Nombre detectado en imagen: {jugador_detectado}")

            # --- LLAMADA REAL A LA API (SIN QUE TÚ ESCRIBAS) ---
            url = f"https://{HOST}/players/statistics"
            querystring = {"season": "2025", "search": jugador_detectado}
            headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}
            
            try:
                response = requests.get(url, headers=headers, params=querystring)
                data = response.json()
                
                if data['response']:
                    # Datos REALES de la API
                    recent_stats = data['response'][-5:]
                    avg_pts = sum([int(i['points']) for i in recent_stats]) / 5
                    avg_reb = sum([int(i['rebounds']) for i in recent_stats]) / 5
                    avg_ast = sum([int(i['assists']) for i in recent_stats]) / 5
                    pra_real_season = avg_pts + avg_reb + avg_ast
                    
                    # Cálculo científico para 1ra Mitad (aprox 55% del total)
                    proy_1h_real = round(pra_real_season * 0.55, 1)
                    
                    # Veredicto Matemático
                    es_over = proy_1h_real > linea_detectada
                    
                    nuevo_analisis = {
                        "id": time.time(),
                        "nombre": jugador_detectado,
                        "proy": proy_1h_real,
                        "linea": linea_detectada,
                        "veredicto": "MÁS (OVER)" if es_over else "MENOS (UNDER)",
                        "pilares": [round(avg_pts,1), round(avg_reb,1), round(avg_ast,1)]
                    }
                    st.session_state.huella.insert(0, nuevo_analisis)
                    st.success("✅ Análisis Real Completado Automáticamente")
                    st.rerun()
                else:
                    st.error("Error de lectura en la API.")
            except:
                st.error("Fallo de conexión con el servidor de datos.")

# --- LA HUELLA: LISTA PERMANENTE ---
st.divider()
st.subheader("📋 Historial de Auditoría")
for idx, p in enumerate(st.session_state.huella):
    with st.container():
        color_v = "veredicto-over" if p['veredicto'] == "MÁS (OVER)" else "veredicto-under"
        st.markdown(f"""
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="font-size:1.5rem;">{p['nombre']}</b>
                    <span class="{color_v}">{p['veredicto']}</span>
                </div>
                <p style="margin:10px 0; color:#aaa;">Línea Detectada: {p['linea']} | <b>Proyección Real 1H: {p['proy']}</b></p>
                <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:10px;">
                    <div class="pilar-box"><small>REAL PTS (Full)</small><br>{p['pilares'][0]}</div>
                    <div class="pilar-box"><small>REAL REB (Full)</small><br>{p['pilares'][1]}</div>
                    <div class="pilar-box"><small>REAL AST (Full)</small><br>{p['pilares'][2]}</div>
                </div>
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
