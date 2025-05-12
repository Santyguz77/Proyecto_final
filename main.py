from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from procesamiento_ia import generar_respuesta
import reconocimiento_voz
import carga_pdf
import re
import pyttsx3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5500", "null", "http://127.0.0.1", "http://localhost:8000", "http://127.0.0.1:5500"]}})
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:5500", "null", "http://127.0.0.1", "http://localhost:8000", "http://127.0.0.1:5500"])

motor_voz = pyttsx3.init()
motor_voz.setProperty("rate", 200)
motor_voz.setProperty("voice", "spanish")

def hablar(texto):
    print(f"🗣️ Hablando: {texto}")
    texto_sin_links = re.sub(r'https?://\S+', '', texto)
    motor_voz.say(texto_sin_links.strip())
    try:
        motor_voz.runAndWait()
    except RuntimeError:
        print("⚠️ El bucle de ejecución ya está en marcha. No se puede ejecutar runAndWait nuevamente.")

pdf_path = r"C:\Users\Asistente\Desktop\Proyecto_Grado\asistente_universidad/Contexto.pdf"
contexto = carga_pdf.extraer_texto_pdf(pdf_path)  

ubicaciones_salones = {
    "lusvin": "imagenes/Amado.jpg",
    "angarita": "imagenes/Angarita.jpg",
    "becerra": "imagenes/Becerra.jpg",
    "botello": "imagenes/Botello.jpg",
    "corzo": "imagenes/Corzo.jpg",
    "diaz": "imagenes/DIAZ.jpg",
    "edificio a": "imagenes/EDIFICIO A.jpg",
    "linares": "imagenes/LINARES.jpg",
    "edificio b": "imagenes/EDIFICIO B.jpg",
    "edificio c": "imagenes/EDIFICIO C.jpg",
    "edificio d": "imagenes/EDIFICIO D.jpg",
    "edificio e": "imagenes/EDIFICIO E.jpg",
    "florez": "imagenes/FLOREZ.jpg",
    "gutierrez": "imagenes/GUTIERREZ.jpg",
    "rector": "imagenes/LENGERKE.jpg",
    "lengerke": "imagenes/LENGERKE.jpg",
    "coordinador": "imagenes/RAFAEL.jpg",
    "rafael": "imagenes/RAFAEL.jpg",
    "lopez": "imagenes/LOPEZ.jpg",
    "marin": "imagenes/MARIN.jpg",
    "murcia": "imagenes/MURCIA.jpg",
    "tutoria": "imagenes/tutorias.jpg",
    "pagina": "imagenes/Pagina.png",
    "oferta": "imagenes/oferta.png",
    "carreras": "imagenes/oferta.png",
    "becas": "imagenes/becas.png",
    "admisiones": "imagenes/admisiones.png",
    "biblioteca": "imagenes/biblioteca.png"    
}

def mostrar_ubicacion(salon):
    img_path = ubicaciones_salones.get(salon)
    if (img_path):
        socketio.emit('mostrar_imagen', {'src': img_path})
    else:
        print(f"No tengo información sobre la ubicación de {salon}")

DESPEDIDAS = ["adiós", "hasta luego", "gracias", "nos vemos", "salir"]

@app.route('/')
def index():
    print("📄 Renderizando la página principal")
    return render_template('interfaz.html')

@socketio.on('pregunta')
def handle_pregunta(data):
    pregunta = data['pregunta']
    metodo = data['metodo']
    
    print(f"📥 Pregunta recibida: {pregunta}, Método: {metodo}")

    if pregunta.lower() in DESPEDIDAS:
        respuesta = "Adiós"
        hablar("Adiós")
        emit('respuesta', {'respuesta': respuesta})
        socketio.sleep(5)
        emit('borrar_mensajes')
        emit('redirigir', {'url': 'Espera.html'})
        return

    try:
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dia_semana_actual = datetime.now().strftime("%A")
        contexto_completo = f"{contexto}\n\nFecha y hora actual: {fecha_hora_actual}\nDía de la semana: {dia_semana_actual}"
        
        respuesta = generar_respuesta(pregunta, contexto_completo)
        print(f"🤖 Respuesta generada: {respuesta}")
    except Exception as e:
        print(f"❌ Error al generar la respuesta: {e}")
        respuesta = "Lo siento, no puedo responder en este momento."

    if metodo == 'voz':
        hablar(respuesta)
    emit('respuesta', {'respuesta': respuesta})

    for salon in ubicaciones_salones.keys():
        if salon.lower() in pregunta.lower():
            mostrar_ubicacion(salon)

@socketio.on('cambiar_metodo')
def handle_cambiar_metodo(data):
    global metodo_interaccion
    metodo_interaccion = data['metodo']
    print(f"🔄 Método de interacción cambiado a: {metodo_interaccion}")

if __name__ == '__main__':
    os.environ['TOGETHER_API_KEY'] = '79a6d9c0813433ab4ca59e6279711b4533fc9a2b34b75d023ea09715225d4537'
    print("🚀 Iniciando la aplicación")
    socketio.run(app, debug=True)

