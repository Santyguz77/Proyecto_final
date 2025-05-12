import together
import os

together.api_key = os.getenv("TOGETHER_API_KEY")

def generar_respuesta(pregunta, contexto):
    if not together.api_key:
        raise ValueError("La clave de API no está configurada. Establece la variable de entorno TOGETHER_API_KEY.")
   
    
   
    prompt = f"""Responde como si fueras un asistente virtual de las Unidades Tecnológicas de Santander (UTS). el saludo debe ser breve. cuando pregunten por un profesor o den el nombre de alguno no digas el horario completo, solo el del dia de hoy.
    Usa tercera persona y sé claro y directo. No inventes información ni agregues datos externos. si te preguntan sobre tu equipo favorito es Millonarios FC. antes de responder que clase tiene hoy algun docente analisa que dia es hoy (no digas hoy es tal dia) y responde si tiene clase o no ese dia. 

    Contexto:
    \"\"\"{contexto}\"\"\" 

    Pregunta: {pregunta}
    Responde en tercera persona y en un solo párrafo:
    """

    try:
        response = together.Completion.create(
            model="deepseek-ai/DeepSeek-V3",
            prompt=prompt,
            max_tokens=200,  
            temperature=0.1, 
            stop=["Pregunta:", "Contexto:", "\n\n"]  
        )
        respuesta = response.choices[0].text.strip()
        # Filtrar contenido en inglés
        if any(word in respuesta.lower() for word in ["okay", "hello", "hi", "thanks"]):
            return "IA: Lo siento, no puedo responder en este momento."
        return respuesta
    except Exception as e:
        return f"IA: Error al generar respuesta: {str(e)}"