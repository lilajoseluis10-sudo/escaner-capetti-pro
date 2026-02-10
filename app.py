# ============================
# NBA SCANNER (BASE)
# ============================

st.divider()
st.header("🏀 Escáner NBA")

player_name = st.text_input("Jugador NBA")
line_value = st.text_input("Línea (ej: 18.5 PRA / 22.5 PTS)")

if st.button("Escanear NBA"):

    if not player_name or not line_value:
        st.warning("Ingresa jugador y línea")
    else:
        st.subheader("Resultado")

        # Lógica inicial simple (no real aún)
        import random
        prob_more = random.randint(48, 72)

        st.write(f"Jugador: **{player_name}**")
        st.write(f"Línea: **{line_value}**")

        if prob_more > 55:
            st.success(f"📈 MORE probable ({prob_more}%)")
        else:
            st.error(f"📉 LESS probable ({100 - prob_more}%)")

        st.info("Módulo NBA activo — siguiente paso: stats reales")
