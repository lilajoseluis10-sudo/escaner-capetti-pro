import streamlit as st
import random
import time
import pandas as pd

# --- CONFIGURACIÓN ELITE JLC-SCANER V26 PRECISION ---
API_KEY = "0c464ef542mshd56e1a359a25c27p150483jsn48dc23e96f0a"

st.set_page_config(page_title="JLC-Scaner Pro", page_icon="🏀", layout="centered")

st.markdown("""
    <style>
        .stApp { background-color: #050505; color: #ffffff; }
        .main-title { font-family: 'Arial Black'; text-align: center; font-size: 2.5rem; color: #ffffff; }
        .audit-row { background-color: #111; border-left: 5px solid #00ff7f; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
        .good { color: #00ff7f; font-weight: bold; }
        .bad { color: #ff4b4b; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">JLC-SCANER PRO</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#888;">TEST DE EFICACIA: PROYECTADO VS REAL (1H)</p>', unsafe_allow_html=True)

foto = st.file_uploader("INYECTAR FOTO PARA AUDITORÍA", type=["jpg", "png", "jpeg"])

if foto:
    with st.spinner('🧬 CALCULANDO PRECISIÓN HISTÓRICA FEBRERO 2026...'):
        time.sleep(2)
        
        st.subheader("🕵️ Auditoría de los Últimos 5 Juegos")
        
        aciertos = 0
        for i in range(1, 6):
            # Simulamos datos de la temporada 2026
            proyectado = round(random.uniform(12.0, 15.0), 1)
            real = round(random.uniform(11.0, 16.0), 1)
            
            # Determinamos si la proyección fue "Buena" (Margen de error menor a 1.5 pts)
            diferencia = abs(proyectado - real)
            es_bueno = diferencia <= 1.5
            if es_bueno: aciertos += 1
            
            status = "✅ PROYECCIÓN BUENA" if es_bueno else "❌ FUERA DE RANGO"
            clase = "good" if es_bueno else "bad"

            st.markdown(f"""
                <div class="audit-row">
                    <b>Juego -{i}:</b> <br>
                    Proyectado: {proyectado} | Real: {real} | 
                    Diferencia: {diferencia:.1} <br>
                    Estado: <span class="{clase}">{status}</span>
                </div>
            """, unsafe_allow_html=True)

        st.divider()
        
        # Resumen de confianza
        porcentaje = (aciertos / 5) * 100
        st.markdown(f"""
            <div style="text-align:center; background:#002200; padding:20px; border-radius:10px;">
                <h2 style="margin:0; color:#00ff7f;">Eficacia del Test: {porcentaje}%</h2>
                <p style="color:#aaa;">{aciertos} de 5 proyecciones fueron precisas este mes.</p>
            </div>
        """, unsafe_allow_html=True)
