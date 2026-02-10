import streamlit as st
import requests
import statistics

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="Capetti Scanner", layout="centered")

st.title("Capetti Ultra Scanner")
st.write("Sistema multicapa estable")

st.write("--------------------------------------------------")

# ===============================
# FUNCIONES SEGURAS
# ===============================

def safe_get_json(url):
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

def parse_line(line_text):
    try:
        parts = line_text.upper().split()
        value = float(parts[0])
        market = parts[1] if len(parts) > 1 else "PRA"
        return value, market
    except:
        return None, None

# ===============================
# OBTENER DATOS REALES
# ===============================

def get_player_data(player):
    search = safe_get_json(f"https://www.balldontlie.io/api/v1/players?search={player}")
    if not search or not search.get("data"):
        return None

    player_id = search["data"][0]["id"]

    season = safe_get_json(f"https://www.balldontlie.io/api/v1/season_averages?player_ids[]={player_id}")
    if not season or not season.get("data"):
        return None

    s = season["data"][0]
    pts = s.get("pts", 0)
    reb = s.get("reb", 0)
    ast = s.get("ast", 0)
    mins = s.get("min", 30)

    season_pra = pts + reb + ast

    games = safe_get_json(f"https://www.balldontlie.io/api/v1/stats?player_ids[]={player_id}&per_page=5")

    last_values = []
    if games and games.get("data"):
        for g in games["data"]:
            try:
                val = g.get("pts", 0) + g.get("reb", 0) + g.get("ast", 0)
                last_values.append(val)
            except:
                pass

    if len(last_values) > 0:
        last_avg = statistics.mean(last_values)
        risk = statistics.pstdev(last_values) if len(last_values) > 1 else 4
    else:
        last_avg = season_pra
        risk = 6

    return {
        "season": season_pra,
        "recent": last_avg,
        "minutes": mins,
        "risk": risk
    }

# ===============================
# SCANNER NBA ULTRA
# ===============================

st.header("NBA Ultra Scanner")

player_name = st.text_input("Jugador NBA")
line_value = st.text_input("Linea (ej: 49.5 PRA)")

if st.button("Escanear"):

    if not player_name or not line_value:
        st.warning("Ingresa jugador y linea")
    else:
        line_num, market = parse_line(line_value)

        if line_num is None:
            st.error("Formato incorrecto")
        else:
            st.write("Analizando...")

            data = get_player_data(player_name)

            if not data:
                st.error("No se encontraron datos")
            else:
                season = data["season"]
                recent = data["recent"]
                mins = data["minutes"]
                risk = data["risk"]

                # MODELO MULTICAPA
                score = (
                    (recent * 0.50) +
                    (season * 0.30) +
                    (mins * 0.10) -
                    (risk * 0.10)
                )

                diff = score - line_num
                confidence = min(max(abs(diff) * 6, 6), 92)

                st.write("Promedio temporada:", round(season,2))
                st.write("Promedio recientes:", round(recent,2))
                st.write("Minutos:", mins)
                st.write("Riesgo:", round(risk,2))

                if diff > 0:
                    st.success("MORE probable - " + str(round(confidence)) + "%")
                else:
                    st.error("LESS probable - " + str(round(confidence)) + "%")

                if risk > 9:
                    st.warning("Jugador inconsistente - riesgo alto")
                elif confidence > 78:
                    st.info("Pick fuerte")
                else:
                    st.info("Pick normal")

st.write("--------------------------------------------------")
st.caption("Capetti Ultra Scanner - Version estable")
