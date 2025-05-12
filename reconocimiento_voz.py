import speech_recognition as sr

def reconocer_voz():
    """Captura audio del micrófono y lo convierte en texto."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Habla ahora... (di algo)")
        recognizer.adjust_for_ambient_noise(source, duration=1)  
        try:
            audio = recognizer.listen(source, timeout=5)  
            texto = recognizer.recognize_google(audio, language="es-ES") 
            print(f"🗣️ Entendido: {texto}")
            return texto
        except sr.WaitTimeoutError:
            print("⏳ No detecté audio. Intenta de nuevo.")
        except sr.UnknownValueError:
            print("❌ No entendí lo que dijiste. Intenta hablar más claro.")
        except sr.RequestError:
            print("⚠️ Error al conectar con el servicio de reconocimiento de voz.")
    return None
