import streamlit as st
import os
from document_parser import extract_text
from diagnostic_engine import analyze_cv_gaps, analyze_linkedin_profile

def main():
    # Configuración de la página
    st.set_page_config(page_title="Optimizador de CV ATS & LinkedIn", page_icon="📄", layout="wide")
    
    # Inicialización de estado en sesión (Preparación para Fase 3 y LinkedIn)
    if "analisis_completado" not in st.session_state:
        st.session_state.analisis_completado = False
    if "brechas_detectadas" not in st.session_state:
        st.session_state.brechas_detectadas = None
    if "linkedin_analizado" not in st.session_state:
        st.session_state.linkedin_analizado = False
    if "linkedin_resultados" not in st.session_state:
        st.session_state.linkedin_resultados = None
        
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuración")
        st.info("Ajusta los parámetros del sistema (Motor LLM Mocked).")
        st.markdown("---")
        st.markdown("Replit Environment Ready ✅")
        
    # Título principal
    st.title("🚀 Optimizador ATS y Perfil Profesional")
    st.markdown("Optimiza tu currículum y perfil de LinkedIn para superar los filtros de reclutadores.")
    st.markdown("---")
    
    tab_cv, tab_linkedin = st.tabs(["📄 Optimizador de CV", "💼 Optimizador de LinkedIn"])
    
    with tab_cv:
        # Layout en columnas para CV
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("1. Carga tu Currículum Base")
            cv_file = st.file_uploader("Sube tu CV actual", type=["pdf", "docx"], key="cv_upload", help="Archivos soportados: .pdf, .docx")
            if cv_file is not None:
                st.success(f"Archivo '{cv_file.name}' cargado.")
                
        with col2:
            st.subheader("2. Ingresa la Oferta Laboral")
            job_description = st.text_area("Descripción del puesto al que aspiras", height=200, 
                                           placeholder="Pega aquí el texto completo de la oferta de trabajo...", key="job_desc_cv")
            
        st.markdown("---")
        
        # Botón de acción principal CV
        if st.button("Analizar Brechas ATS (Ejecutar Fase 2)", type="primary", key="btn_cv"):
            if not cv_file:
                st.error("⚠️ Por favor, carga un archivo de currículum base para continuar.")
            elif not job_description.strip():
                st.error("⚠️ Por favor, ingresa el texto de la oferta laboral.")
            else:
                with st.spinner("Analizando tu CV contra la oferta laboral... (Simulación LLM)"):
                    try:
                        # 1. Extraer texto del CV
                        cv_text = extract_text(cv_file)
                        
                        # 2. Diagnóstico a través de Motor ATS
                        resultado_analisis = analyze_cv_gaps(cv_text, job_description)
                        
                        # 3. Guardar estado
                        st.session_state.cv_text_original = cv_text
                        st.session_state.brechas_detectadas = resultado_analisis.get("brechas", [])
                        st.session_state.analisis_completado = True
                        
                    except Exception as e:
                        st.error(f"Se produjo un error durante el análisis: {e}")

        # Mostrar resultados si el análisis fue completado
        if st.session_state.analisis_completado and st.session_state.brechas_detectadas:
            st.success("✅ Análisis completado con éxito. Se han identificado las siguientes brechas:")
            
            st.subheader("🔍 Diagnóstico del Perfil vs Oferta Laboral")
            for i, brecha in enumerate(st.session_state.brechas_detectadas, start=1):
                with st.expander(f"Brecha {i}: {brecha['competencia']}", expanded=True):
                    st.markdown(f"**Lo que pide la oferta:** {brecha['descripcion_oferta']}")
                    st.markdown(f"**Estado en tu CV actual:** {brecha['estado_cv_actual']}")
            
            st.markdown("---")
            st.subheader("✍️ Cuestionario de Resolución de Brechas (Método STAR)")
            st.markdown("Para cada brecha detectada, describe brevemente una experiencia real que demuestre tu competencia. Intenta estructurarla en formato **STAR**: **S**ituación, **T**area, **A**cción y **R**esultado.")
            
            # Diccionario para guardar respuestas del formulario
            respuestas_usuario = {}
            
            with st.form("star_form"):
                for i, brecha in enumerate(st.session_state.brechas_detectadas, start=1):
                    st.markdown(f"**{i}. {brecha['competencia']}**")
                    respuestas_usuario[brecha['competencia']] = st.text_area(
                        f"Tu experiencia (Brecha {i}):",
                        key=f"input_brecha_{i}",
                        placeholder="Ej: En mi trabajo anterior (S/T), implementé la herramienta X (A), reduciendo el tiempo de carga un 20% (R)..."
                    )
                    st.markdown("---")
                    
                submit_star = st.form_submit_button("Generar Puntos STAR para el CV (Ejecutar Fase 3)", type="primary")
                
            if submit_star:
                with st.spinner("Redactando 'bullet points' profesionales de alto impacto... (Simulación LLM)"):
                    from rewrite_engine import rewrite_bullet_star
                    
                    bullets_generados = []
                    for comp, resp in respuestas_usuario.items():
                        if resp.strip():
                            try:
                                bullet = rewrite_bullet_star(comp, resp)
                                bullets_generados.append({"competencia": comp, "bullet": bullet})
                            except Exception as e:
                                st.error(f"Error procesando '{comp}': {e}")
                    
                    st.session_state.bullets_generados = bullets_generados
                    st.session_state.fase_3_completada = True

        # Mostrar resultados generados por el motor de reescritura
        if st.session_state.get("fase_3_completada", False) and st.session_state.get("bullets_generados"):
            st.success("✅ Puntos del currículum generados exitosamente.")
            st.subheader("✨ Resultados Optimizados para tu CV")
            
            for item in st.session_state.bullets_generados:
                st.markdown(f"- **[{item['competencia']}]**: {item['bullet']}")
                
            st.markdown("---")
            st.subheader("📥 Paso Final: Descargar CV Optimizado")
            st.markdown("Haz clic en el botón de abajo para descargar tu nuevo documento en formato DOCX. Hemos fusionado tu texto original con estas nuevas adiciones ATS-friendly.")
            
            from exporter import generate_optimized_cv_docx
            try:
                docx_buffer = generate_optimized_cv_docx(
                    st.session_state.get("cv_text_original", ""),
                    st.session_state.bullets_generados
                )
                
                st.download_button(
                    label="⬇️ Descargar Currículum ATS Optimizado (.docx)",
                    data=docx_buffer,
                    file_name="CV_Optimizado_ATS.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    type="primary"
                )
            except Exception as e:
                st.error(f"Error al preparar el documento para descarga: {e}")

    with tab_linkedin:
        st.markdown("### Optimiza tu Perfil de LinkedIn")
        st.markdown("Sube tu perfil exportado en PDF o pega directamente el texto para recibir recomendaciones personalizadas para hacer match con los reclutadores.")
        
        col_lin1, col_lin2 = st.columns(2)
        
        with col_lin1:
            st.subheader("1. Tu Perfil Actual")
            input_method = st.radio("Método de ingreso:", ["Subir PDF de LinkedIn", "Pegar Texto"], key="linkedin_input_method")
            
            linkedin_text_final = ""
            if input_method == "Subir PDF de LinkedIn":
                linkedin_file = st.file_uploader("Sube tu perfil (PDF)", type=["pdf"], key="linkedin_upload")
                if linkedin_file:
                    st.success("PDF cargado. Usaremos su contenido para el análisis.")
                    try:
                        linkedin_text_final = extract_text(linkedin_file)
                    except Exception as e:
                        st.error("Error al extraer texto del PDF.")
            else:
                linkedin_text_final = st.text_area("Pega aquí el texto de tu perfil", height=150, key="linkedin_text_paste")
                
        with col_lin2:
            st.subheader("2. Oferta o Rol Deseado")
            job_description_lin = st.text_area("Descripción de la oferta laboral o rol objetivo", height=150, 
                                           placeholder="Ej: Busco rol de Ingeniero de Software Senior especializado en React y Node...", key="job_desc_lin")
                                           
        st.markdown("---")
        
        if st.button("Optimizar Perfil de LinkedIn", type="primary", key="btn_linkedin"):
            if not linkedin_text_final.strip():
                st.error("⚠️ Por favor, ingresa tu perfil de LinkedIn (por PDF o texto).")
            elif not job_description_lin.strip():
                st.error("⚠️ Por favor, ingresa la oferta laboral o rol deseado.")
            else:
                with st.spinner("Analizando tu perfil para el algoritmo de LinkedIn..."):
                    try:
                        resultados_lin = analyze_linkedin_profile(linkedin_text_final, job_description_lin)
                        st.session_state.linkedin_resultados = resultados_lin
                        st.session_state.linkedin_analizado = True
                    except Exception as e:
                        st.error(f"Error al analizar el perfil: {e}")
                        
        if st.session_state.linkedin_analizado and st.session_state.linkedin_resultados:
            st.success("✅ Análisis completado. Aquí tienes tus recomendaciones para destacar en LinkedIn.")
            
            res = st.session_state.linkedin_resultados
            
            st.markdown("#### 🔹 Titular (Headline) Propuesto")
            st.info(res.get("headline_propuesto", ""))
            
            st.markdown("#### 🔹 Acerca de (About) Optimizado")
            st.info(res.get("about_propuesto", ""))
            
            st.markdown("#### 🔹 Aptitudes Clave (Skills) a Agregar")
            for skill in res.get("aptitudes_sugeridas", []):
                st.markdown(f"- {skill}")
                
            st.markdown("---")
            st.markdown("💡 **Tip:** Copia estos textos y actualiza tu perfil directamente en LinkedIn. Asegúrate de pedir recomendaciones a tus ex-compañeros para validar estas nuevas aptitudes.")

if __name__ == "__main__":
    main()
