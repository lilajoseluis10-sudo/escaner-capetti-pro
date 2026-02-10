import streamlit as st
import pytesseract
from PIL import Image

st.title("🏀 Escáner Capetti - NBA Sharp")

# Subir la captura de PrizePicks
file = st.file_uploader("Sube tu captura de NBA", type=['png', 'jpg', 'jpeg'])

if file:
    img = Image.open(file)
    st.image(img, caption="Analizando...")
    
    # El escáner intenta leer los nombres de los jugadores
    with st.spinner("Buscando jugadores..."):
        text = pytesseract.image_to_string(img).lower()
        
        st.write("### 🔍 Veredicto del Escáner")
        
        # Lógica de hoy: 10 de Feb, 2026
        if "lebron" in text or "reaves" in text:
            st.warning("⚠️ ALERTA LAKERS: Jugando Back-to-Back. Línea de Reaves (25.7 pts) inflada por baja de Luka.")
        
        if "haliburton" in text:
            st.error("🚨 BAJA CONFIRMADA: Haliburton OUT. No apuestes a sus puntos.")
            
        if "fox" in text:
            st.success("✅ VALOR DETECTADO: Fox vs Lakers cansados. Proyección de +6.5 asistencias.")
        
        st.info("Texto detectado en la imagen: " + text[:100] + "...")
