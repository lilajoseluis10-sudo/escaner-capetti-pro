# ===============================
# NBA SCANNER ELITE — PASO 1
# ===============================
import requests
import statistics

st.header("🏀 Escáner NBA ELITE")

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

def get_player_data(player):
    try:
        search_url = f"https://www.balldontlie.io/api/v1/players?search={player}"
        r = requests.get(search_url, timeout=10)
        data = r.json()
        if not data["data"]:
            return None
        player_id = data["data"][0]["id"]

        # Temporada
        stats_url = f"https://www.balldontlie.io/api/v1/season_averages?player_ids[]={player_id}"
        r2 = requests.get(stats_url, timeout=10)
        stats = r2.json()["data"]
        if not stats:
            return None
        s = stats[0]

        pts = s["pts"]
        reb = s["reb"]
        ast = s["ast"]
        pra = pts + reb + ast
        mins = s["min"]

        # Últimos juegos
        games_url = f"https://www.balldontlie.io/api/v1/stats?player_ids[]={player_id}&per_page=5"
        r3 = requests.get(games_url, timeout=10)
        games = r3.json()["data"]

        last_values = []
        for g in games:
            if g["min"] is None:
                continue
            last_values.append(g["pts"] + g["reb"] + g["ast"])

        if len(last_values) == 0:
            last_avg = pra
            consistency = 0
        else:
            last_avg = statistics.mean(last_values)
            consistency = statistics.pstdev(last_values)

        return {
            "season_pra": pra,
            "last_avg": last_avg,
            "minutes": mins,
            "consistency": consistency
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
            st.write("Analizando datos reales...")
            data = get_player_data(player_name)

            if not data:
                st.error("No se encontraron datos del jugador")
            else:
                season = data["season_pra"]
                recent = data["last_avg"]
                mins = data["minutes"]
                consistency = data["consistency"]

                # Score multicapa
                score = (
                    (recent * 0.45) +
                    (season * 0.35) +
                    (mins * 0.10) -
                    (consistency * 0.10)
                )

                diff = score - line_num
                confidence = min(max(abs(diff) * 7, 6), 92)

                st.subheader("Resultado Scanner ELITE")

                st.write(f"Promedio temporada: **{round(season,2)}**")
                st.write(f"Promedio últimos juegos: **{round(recent,2)}**")
                st.write(f"Minutos promedio: **{mins}**")
                st.write(f"Consistencia (riesgo): **{round(consistency,2)}**")

                if diff > 0:
                    st.success(f"📈 MORE probable ({round(confidence)}%)")
                else:
                    st.error(f"📉 LESS probable ({round(confidence)}%)")

                if consistency > 8:
                    st.warning("⚠️ Jugador inconsistente — riesgo alto")
                elif confidence > 75:
                    st.info("🔥 Pick fuerte")
                else:
                    st.info("Pick estándar")
