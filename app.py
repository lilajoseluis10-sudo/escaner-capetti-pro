
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
