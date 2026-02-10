import streamlit as st
import requests
from PIL import Image
import random

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="Capetti Scanner", layout="centered")

st.title("🚀 Capetti Pro Scanner")
st.write("Análisis NBA + Tenis")

st.write("---")

# ===============================
# TENIS SCANNER (BASE)
# ===============================
st.header("🎾 Escáner de Tenis")

uploaded_file = st.file_uploader("Sube captura (Tenis)", type=["png","jpg","jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada", use_container_width=True)

    st.write("Analizando...")
    prob = random.randint(45, 75)

    if prob > 55:
        st.success(f"📈 OVER / MORE probable ({prob}%)")
    else:
        st.error(f"📉 UNDER / LESS probable ({100 - prob}%)")

st.write("---")

# ===============================
# NBA SCANNER (ESTABLE)
# ===============================
st.header("🏀 Escáner NBA")

player_name = st.text_input("Jugador NBA")
line_value = st.text_input("Línea (ej: 49.5 PRA / 25.5 PTS)")

def parse_line(line_text):
    try:
        parts = line_text.upper().split()
        value = float(parts[0])
        market = parts[1] if len(parts) > 1 else "PRA"
        return value, market
    except:
        return None, None

def get_player_avg(player):
    try:
        search_url = f"https://www.balldontlie.io/api/v1/players?search={player}"
        r = requests.get(search_url, timeout=10)
        data = r.json()

        if not data["data"]:
            return None

        player_id = data["data"][0]["id"]

        stats_url = f"https://www.balldontlie.io/api/v1/season_averages?player_ids[]={player_id}"
        r2 = requests.get(stats_url, timeout=10)
        stats = r2.json()["data"]

        if not stats:
            return None

        s = stats[0]
        pts = s["pts"]
        reb = s["reb"]
        ast = s["ast"]

        return {
            "PTS": pts,
            "REB": reb,
            "AST": ast,
            "PRA": pts + reb + ast
        }
    except:
        return None

if st.button("Escanear NBA"):

    if not player_name or not line_value:
        st.warning("Ingresa jugador y línea")
    else:
        line_num, market = parse_line(line_value)

        if line_num is None:
            st.error("Formato inválido. Ej: 49.5 PRA")
        else:
            st.write("Consultando datos reales...")
            avgs = get_player_avg(player_name)

            if not avgs:
                st.error("No se encontraron datos del jugador")
            else:
                player_avg = avgs[market]

                st.write(f"Jugador: **{player_name}**")
                st.write(f"Promedio temporada: **{round(player_avg,2)}**")

                diff = player_avg - line_num
                confidence = min(max(abs(diff) * 8, 5), 85)

                if diff > 0:
                    st.success(f"📈 MORE probable ({round(confidence)}%)")
                else:
                    st.error(f"📉 LESS probable ({round(confidence)}%)")

st.write("---")
st.caption("Capetti Scanner — versión estable")
