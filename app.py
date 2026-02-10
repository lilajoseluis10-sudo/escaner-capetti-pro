# ===============================
# NBA SCANNER (DATOS REALES - BALLDONTLIE)
# ===============================
import requests

st.header("🏀 Escáner NBA")

player_name = st.text_input("Jugador NBA")
line_value = st.text_input("Línea (ej: 18.5 PRA / 22.5 PTS)")

def parse_line(line_text: str):
    """
    Extrae número y tipo de mercado.
    Ejemplos:
      '18.5 PRA' -> (18.5, 'PRA')
      '22.5 PTS' -> (22.5, 'PTS')
    """
    try:
        parts = line_text.upper().split()
        value = float(parts[0])
        market = parts[1] if len(parts) > 1 else "PRA"
        return value, market
    except:
        return None, None

def get_player_season_avg(player_query: str):
    """
    Busca jugador y devuelve promedios de la temporada:
    PTS, REB, AST, PRA
    """
    try:
        # 1) Buscar jugador
        search_url = f"https://www.balldontlie.io/api/v1/players?search={player_query}"
        r = requests.get(search_url, timeout=10)
        data = r.json()
        if not data.get("data"):
            return None

        player_id = data["data"][0]["id"]

        # 2) Stats temporada actual (última disponible)
        stats_url = f"https://www.balldontlie.io/api/v1/season_averages?player_ids[]={player_id}"
        r2 = requests.get(stats_url, timeout=10)
        stats = r2.json().get("data", [])
        if not stats:
            return None

        s = stats[0]
        pts = s.get("pts", 0)
        reb = s.get("reb", 0)
        ast = s.get("ast", 0)
        pra = pts + reb + ast

        return {
            "PTS": pts,
            "REB": reb,
            "AST": ast,
            "PRA": pra
        }
    except:
        return None

if st.button("Escanear NBA"):

    if not player_name or not line_value:
        st.warning("Ingresa jugador y línea (ej: 18.5 PRA)")
    else:
        line_num, market = parse_line(line_value)

        if line_num is None:
            st.error("Formato de línea inválido. Ej: 18.5 PRA / 22.5 PTS")
        else:
            with st.spinner("Consultando datos reales..."):
                avgs = get_player_season_avg(player_name)

            if not avgs:
                st.error("No se encontraron datos del jugador.")
            else:
                player_avg = avgs.get(market, None)

                st.subheader("Resultado Scanner")
                st.write(f"Jugador: **{player_name}**")
                st.write(f"Mercado: **{market}**")
                st.write(f"Línea: **{line_num}**")
                st.write(f"Promedio temporada: **{round(player_avg,2)}**")

                # Proyección simple vs línea
                diff = player_avg - line_num
                confidence = min(max(abs(diff) * 8, 5), 85)  # escala simple

                if diff > 0:
                    st.success(f"📈 MORE probable ({round(confidence)}%)")
                else:
                    st.error(f"📉 LESS probable ({round(confidence)}%)")

                st.info("Modelo base con promedios de temporada (siguiente: últimos 5, minutos, rival, pace)")
