# NOTA: En Replit/Producción se utilizaría una librería como openai
# import openai

SYSTEM_PROMPT_REWRITE = """
Eres un Experto Redactor de Currículums y especialista en Reclutamiento.
Tu tarea es tomar la información provista por el usuario sobre una experiencia laboral para cubrir una brecha, y redactarla como un "bullet point" profesional y de alto impacto para un currículum, utilizando estrictamente el método STAR (Situación, Tarea, Acción, Resultado).

REGLAS:
1. Sé conciso, profesional y directo. Comienza con un verbo de acción fuerte (ej. Lideré, Implementé, Diseñé).
2. Incluye métricas y resultados cuantificables basándote ÚNICAMENTE en lo que el usuario provee.
3. NO INVENTES DATOS (Cero alucinaciones). Si el usuario no da métricas, no las inventes.
4. El resultado debe ser una sola oración estructurada, lista para copiar y pegar en un CV.
"""

def rewrite_bullet_star(competencia: str, user_input: str) -> str:
    """
    Toma el input del usuario y la competencia a cubrir, y genera un bullet point usando el framework STAR.
    """
    if not user_input.strip():
        return ""
        
    try:
        # AQUÍ IRÍA LA LLAMADA REAL AL LLM
        # Ejemplo:
        # prompt = f"Competencia: {competencia}\nExperiencia del usuario: {user_input}"
        # response = client.chat.completions.create(...)
        # return response.choices[0].message.content
        
        # --- SIMULACIÓN PARA FASE DE DESARROLLO (MOCK DATA) ---
        import time
        time.sleep(1) # Simula latencia
        
        # Generamos una respuesta de prueba basada en la entrada del usuario
        return f"Dirigí iniciativas de {competencia}, aplicando las siguientes acciones: '{user_input[:50]}...', logrando cerrar la brecha eficientemente (Mock STAR Bullet)."
        
    except Exception as e:
        raise Exception(f"Error al reescribir la experiencia: {str(e)}")
