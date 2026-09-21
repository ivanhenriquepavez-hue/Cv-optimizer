import json

# NOTA: En Replit/Producción se utilizaría una librería como openai
# import openai
# from openai import OpenAI

SYSTEM_PROMPT = """
Eres un Sistema Experto de Reclutamiento y Arquitecto ATS (Applicant Tracking System).
Tu objetivo es analizar un currículum base y compararlo contra una oferta laboral específica.

REGLAS INQUEBRANTABLES:
1. CERO ALUCINACIONES: Tienes estrictamente prohibido inventar, suponer o agregar habilidades, experiencias, educación o logros que no estén presentes explícita o implícitamente en el texto del currículum original.
2. TU ÚNICA TAREA ES IDENTIFICAR BRECHAS: Identifica exactamente 5 competencias, herramientas o requisitos clave mencionados en la oferta laboral que NO están claramente reflejados, justificados o cuantificados en el currículum base.
3. FORMATO DE SALIDA: El output debe estar estructurado en formato JSON estrictamente válido, sin texto adicional fuera del JSON, con la siguiente estructura:
{
    "brechas": [
        {
            "competencia": "Nombre de la competencia o requisito",
            "descripcion_oferta": "Breve explicación de cómo se exige en la oferta laboral.",
            "estado_cv_actual": "Explicación de por qué el CV actual presenta una brecha al respecto (ej. no se menciona, falta cuantificar, se menciona vagamente)."
        }
    ] # Asegúrate de que sean exactamente 5 elementos
}
"""

def analyze_cv_gaps(cv_text: str, job_description: str) -> dict:
    """
    Compara el texto extraído del CV contra la descripción del puesto.
    Retorna un diccionario estructurado (JSON parseado) con las 5 brechas clave.
    """
    if not cv_text.strip() or not job_description.strip():
        raise ValueError("El texto del CV o la oferta laboral están vacíos.")

    prompt_usuario = f"""
    --- CURRÍCULUM BASE ---
    {cv_text}
    
    --- OFERTA LABORAL ---
    {job_description}
    """
    
    try:
        # AQUÍ IRÍA LA LLAMADA REAL A LA API DEL LLM (OpenAI, Anthropic, etc.)
        # Ejemplo:
        # client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        # response = client.chat.completions.create(...)
        # result = json.loads(response.choices[0].message.content)
        
        # --- SIMULACIÓN PARA FASE DE DESARROLLO (MOCK DATA) ---
        # Simulamos una respuesta de la API para construir la UI y la Fase 3.
        import time
        time.sleep(1.5) # Simulando latencia de inferencia
        
        mock_result = {
            "brechas": [
                {
                    "competencia": "Gestión de Proyectos Ágiles",
                    "descripcion_oferta": "Se requiere experiencia liderando sprints bajo marcos Agile/Scrum.",
                    "estado_cv_actual": "Se menciona 'Gestión de proyectos' de forma general, pero no se especifica la metodología ni el liderazgo de sprints."
                },
                {
                    "competencia": "Análisis de Datos con Python/Pandas",
                    "descripcion_oferta": "Necesario para generar reportes analíticos para stakeholders.",
                    "estado_cv_actual": "El CV lista 'Python' como habilidad, pero no menciona experiencia aplicada en análisis de datos o el uso de Pandas."
                },
                {
                    "competencia": "Liderazgo y Gestión de Equipos",
                    "descripcion_oferta": "Coordinación de equipos multidisciplinarios de más de 5 personas.",
                    "estado_cv_actual": "Menciona ser 'Ingeniero Senior', pero no destaca responsabilidades de gestión, mentoría o tamaño del equipo liderado."
                },
                {
                    "competencia": "Optimización de Rendimiento (Web/Cloud)",
                    "descripcion_oferta": "Experiencia mejorando tiempos de carga, latencia o escalabilidad de sistemas.",
                    "estado_cv_actual": "Se describen tareas de mantenimiento, pero no hay logros cuantificados sobre optimizaciones de rendimiento en sistemas."
                },
                {
                    "competencia": "Inglés Avanzado (B2/C1)",
                    "descripcion_oferta": "Comunicación técnica fluida en inglés con clientes internacionales.",
                    "estado_cv_actual": "No se incluye ninguna sección de idiomas en el currículum, lo que genera dudas sobre el nivel requerido."
                }
            ]
        }
        return mock_result
        
    except Exception as e:
        raise Exception(f"Error interno en el motor de diagnóstico ATS: {str(e)}")

def analyze_linkedin_profile(linkedin_text: str, job_description: str) -> dict:
    """
    Analiza un perfil de LinkedIn contra una descripción de puesto.
    Retorna sugerencias para Titular, Acerca de y Aptitudes.
    """
    if not linkedin_text.strip() or not job_description.strip():
        raise ValueError("El texto del perfil o la oferta laboral están vacíos.")
        
    try:
        import time
        time.sleep(1.5) # Simulando latencia de inferencia
        
        mock_result = {
            "headline_propuesto": "Senior Software Engineer | Python, React & Cloud Architecture | Transformando ideas en productos escalables",
            "about_propuesto": "Soy un ingeniero de software con más de 5 años de experiencia liderando equipos técnicos y construyendo aplicaciones escalables. Mi pasión es resolver problemas complejos utilizando tecnologías modernas como Python, AWS y React.\\n\\nMe especializo en arquitecturas orientadas a microservicios y metodologías ágiles. Siempre estoy buscando aprender y compartir conocimientos con la comunidad.",
            "aptitudes_sugeridas": [
                "Python (Programación Orientada a Objetos)",
                "Amazon Web Services (AWS)",
                "Arquitectura de Microservicios",
                "Metodologías Ágiles (Scrum)",
                "React.js"
            ]
        }
        return mock_result
        
    except Exception as e:
        raise Exception(f"Error interno en el motor de LinkedIn: {str(e)}")
