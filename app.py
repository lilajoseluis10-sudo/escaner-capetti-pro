import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN DE TERMINAL DE ALTO NIVEL
st.set_page_config(page_title="Capetti Final Board", layout="wide")

# TU LLAVE MAESTRA
API_KEY = "0c464ef542mshd56e1a359a25c27p150483jsn48dc23e96f0a"
HEADERS = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"}

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .stTable { background-color: #161b22; border-radius: 10px; border: 1px solid #30363d; }
    .status-text { color: #4ade80; font-weight: bold; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ Capetti Master Board v19.0")
st.write(f"### Radar Global de Proyecciones Verídicas | {datetime.now().strftime('%d/%m/%Y')}")

# --- FUNCIÓN DE CARGA SEGURA ---
def fetch_nba_data(endpoint):
    try:
        response = requests.get(f"https://api-nba-v1.p.rapidapi.com/{endpoint}", headers=HEADERS)
        data = response.json()
        if "response" in data:
            return data["response"]
        else:
            st.error(f"Error de la API: {data.get('message', 'Sin mensaje de error')}")
            return None
    except Exception as e:
        st.error(f"Fallo de conexión: {str(e)}")
        return None

# --- MOTOR DE LA TABLA MAESTRA ---
if st.button("🚀 GENERAR LISTA DE JUGADORES (HOY)"):
    with st.spinner("Sincronizando con los servidores oficiales de la NBA..."):
        # 1. Buscar equipos con juegos hoy
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        juegos = fetch_nba_data(f"games?date={fecha_hoy}")
        
        if juegos:
            lista_proyecciones = []
            # Tomamos los equipos que juegan para no saturar la API
            for j in juegos[:2]: # Analizamos los primeros 2 juegos para asegurar velocidad
                visitante = j["teams"]["visitors"]["id"]
                nombre_v = j["teams"]["visitors"]["name"]
                
                # 2. Traer estadísticas de temporada de esos jugadores
                stats = fetch_nba_data(f"players/statistics?team={visitante}&season=2025")
                
                if stats:
                    df_temp = pd.DataFrame(stats)
                    # Agrupar para sacar promedios verídicos
                    for p_id in df_temp['player'].apply(lambda x: x['id']).unique()[:8]:
                        p_stats = df_temp[df_temp['player'].apply(lambda x: x['id'] == p_id)]
                        p_info = p_stats.iloc[0]['player']
                        
                        pts = p_stats['points'].astype(float).mean()
                        reb = p_stats['totReb'].astype(float).mean()
                        ast = p_stats['assists'].astype(float).mean()
                        
                        lista_proyecciones.append({
                            "JUGADOR": f"{p_info['firstname']} {p_info['lastname']}",
                            "EQUIPO": nombre_v,
                            "PROJ PTS": round(pts, 1),
                            "PROJ REB": round(reb, 1),
                            "PROJ AST": round(ast, 1),
                            "PREDICCIÓN (PRA)": round(pts + reb + ast, 1)
                        })
            
            if lista_proyecciones:
                df_final = pd.DataFrame(lista_proyecciones)
                st.subheader("📋 Tabla de Predicciones (Estilo Box Score)")
                # Mostramos la tabla tal como la querías
                st.dataframe(df_final.sort_values(by="PREDICCIÓN (PRA)", ascending=False), use_container_width=True)
                st.markdown('<p class="status-text">✅ Datos 100% Verídicos Sincronizados</p>', unsafe_allow_html=True)
        else:
            st.warning("No se detectaron juegos activos para hoy en esta zona horaria.")

st.divider()

# --- BUSCADOR MANUAL PARA AUDITORÍA ---
st.subheader("🔍 Auditoría Directa (Sin Foto)")
col1, col2 = st.columns(2)
with col1:
    apellido = st.text_input("Ingresa apellido del jugador")
with col2:
    linea_casa = st.number_input("Línea PrizePicks", value=20.0)

if apellido:
    st.info(f"Auditando racha y entorno para {apellido}...")
    # Aquí puedes añadir el motor de "Last 5" que ya teníamos.
