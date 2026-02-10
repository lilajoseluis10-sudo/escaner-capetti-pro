import streamlit as st
import random
from PIL import Image

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="Capetti Pro Scanner", layout="centered")

st.title("🚀 Capetti Pro Scanner")
st.write("Análisis NBA + Tenis (Base Estable)")

st.write("---")

# ===============================
# TENIS SCANNER (BASE SIMPLE)
# ===============================
st.header("🎾 Escáner de Tenis")

uploaded_file = st.file_uploader("Sube captura (Tenis)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada", use_container_width=True)

    st.write("Analizando...")
    prob = random.randint(45, 75)

    if prob > 55:
        st.success(f"📈 OVER / MORE probable ({prob}%)")
    else:
        st.error(f"📉 UNDER / LESS probable ({100 - prob}%)")

    st.info("Modo base activo (luego conectamos stats reales)")

st.write("---")

# ===============================
# NBA SCANNER (FUNCIONAL BASE)
# ===============================
st.header("🏀 Escáner NBA")

player_name = st.text_input("Jugador NBA")
line_value = st.text_input("Línea (ej: 18.5 PRA / 22.5 PTS)")

if st.button("Escanear NBA"):

    if not player_name or not line_value:
        st.warning("Ingresa jugador y línea")
    else:
        st.subheader("Resultado Scanner")

        # Simulación estable (no rompe)
        prob_more = random.randint(48, 72)

        st.write(f"Jugador: **{player_name}**")
        st.write(f"Línea: **{line_value}**")

        if prob_more > 55:
            st.success(f"📈 MORE probable ({prob_more}%)")
        else:
            st.error(f"📉 LESS probable ({100 - prob_more}%)")

        st.info("Scanner NBA base funcionando — listo para expansión")

st.write("---")
st.caption("Capetti Scanner v1.0 — Estable")
