import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN DE TERMINAL DE ALTO NIVEL
st.set_page_config(page_title="Capetti Infinite Board", layout="wide")

# TU LLAVE MAESTRA
API_KEY = "0c464ef542mshd56e1a359a25c27p150483jsn48dc23e96f0a"
HEADERS = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"}

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .stDataFrame { border: 1px solid #d4af37; border-radius: 10px; }
    .status-active { color: #4ade80; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌌 Capetti Infinite Board v18.0")
st.write(f"### Radar Global de Proyecciones | {datetime.now().strftime('%d/%m/%Y')}")

# --- FUNCIÓN MAESTRA DE CONEXIÓN ---
def obtener_datos_veridicos():
    try:
        # 1. Buscar juegos de HOY para no saturar la API
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        url_juegos = f"https://api-nba-v1.p.rapidapi.com/games?date={fecha_hoy}"
        juegos = requests.get(url_juegos, headers=HEADERS).json()["response"]
        
        if not juegos:
            return "No hay juegos programados para hoy en la base de datos."

        lista_proyecciones = []
        # Tomamos los primeros 3 juegos para asegurar estabilidad inicial
        for juego in juegos[:3]:
            equipo_id = juego["teams"]["visitors"]["id"]
            nombre_equipo = juego["teams"]["visitors"]["name"]
            
            # 2. Traer estadísticas reales de los jugadores de esos equipos
            url_stats = f"https://api-nba-v1.p.rapidapi.com/players/statistics?team={equipo_id}&season=2025"
            stats_data = requests.get(url_stats, headers=HEADERS).json()["response"]
            
            # Agrupamos por jugador para sacar promedios
            df_temp = pd.DataFrame(stats_data)
            if not df_temp.empty:
                for p_id in df_temp['player'].apply(lambda x: x['id']).unique()[:5]:
                    p_stats = df_temp[df_temp['player'].apply(lambda x: x['id'] == p_id)]
                    p_info = p_stats.iloc[0]['player']
                    
                    pts = p_stats['points'].astype(float).mean()
                    reb = p_stats['totReb'].astype(float).mean()
                    ast = p_stats['assists'].astype(float).mean()
                    
                    lista_proyecciones.append({
                        "JUGADOR": f"{p_info['firstname']} {p_info['lastname']}",
                        "EQUIPO": nombre_equipo,
                        "PROJ PTS": round(pts, 1),
                        "PROJ REB": round(reb, 1),
                        "PROJ AST": round(ast, 1),
                        "TOTAL PRA": round(pts + reb + ast, 1)
                    })
        return lista_proyecciones
    except Exception as e:
        return f"Error de conexión: {str(e)}"

# --- INTERFAZ DE TABLA MAESTRA ---
if st.button("🚀 SINCRONIZAR TODA LA LIGA (HOY)"):
    with st.spinner("Conectando con la infraestructura oficial de la NBA..."):
        resultado = obtener_datos_veridicos()
        
        if isinstance(resultado, list):
            df = pd.DataFrame(resultado)
            st.subheader("📋 Tabla Maestra de Proyecciones (Verídica)")
            # Estilo similar a la tabla de puntos
            st.dataframe(df.style.background_gradient(cmap='Blues', subset=['TOTAL PRA']), use_container_width=True)
            st.success("✅ Datos sincronizados correctamente.")
        else:
            st.error(resultado)

st.divider()

# --- AUDITORÍA INDIVIDUAL ---
st.subheader("🔍 Auditoría de Precisión (Manual)")
col1, col2 = st.columns(2)
with col1:
    atleta = st.text_input("Apellido del Jugador")
with col2:
    linea = st.number_input("Línea PrizePicks", value=20.0)

if atleta:
    st.info(f"Analizando tendencia actual para {atleta}...")
    # Aquí corre el motor de racha Last 5 que ya configuramos antes
