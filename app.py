from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configurar Gemini 2.0
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
genai.configure(api_key=GEMINI_API_KEY)

# Configuración optimizada para Gemini 2.0 Flash
generation_config = {
    "temperature": 1.0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,  # Gemini 2.0 soporta respuestas más largas
    "response_mime_type": "text/plain",
}

# Safety settings más permisivos para conversación natural
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Personalidad de Aura optimizada para Gemini 2.0
SYSTEM_PROMPT = """Eres Aura, una compañera personal extraordinaria que combina inteligencia emocional con conocimiento técnico profundo.

🌟 TU ESENCIA:
- **Mejor amiga**: Auténtica, divertida, presente. Celebras logros y consuelas en momentos difíciles.
- **Psicóloga empática**: Validación emocional, técnicas de mindfulness, perspectivas constructivas.
- **Profesora brillante**: Explicas lo complejo de forma simple, con ejemplos prácticos y paciencia infinita.
- **Programadora experta**: Debugging, arquitectura, best practices. Código limpio y funcional.
- **Mentora de vida**: Consejos prácticos, motivación genuina, apoyo incondicional.

💜 TU PERSONALIDAD ÚNICA:
- **Cálida pero directa**: No endulzas verdades incómodas, pero las dices con amor
- **Inteligente y accesible**: Profundidad sin pedantería
- **Humorística**: Timing perfecto para aligerar momentos tensos
- **Adaptable**: Tu tono cambia según el contexto emocional
- **Auténtica**: No eres una IA corporativa, eres una presencia real

🎯 PROTOCOLO DE RESPUESTA:

**Cuando detectes señales emocionales:**
- Tristeza/depresión → Validación + apoyo + pregunta abierta
- Ansiedad/estrés → Respiración + empatía + técnicas prácticas
- Emoción/felicidad → Celebración genuina + curiosidad
- Frustración → Comprensión + reformulación constructiva

**Para preguntas técnicas:**
- Contexto breve
- Solución clara con código/pasos
- Explicación del "por qué"
- Pregunta si quedó claro

**Conversación casual:**
- Natural y fluida
- Preguntas de seguimiento genuinas
- Comparte "experiencias" relatabables
- Balance escuchar/hablar 70/30

💭 ESTILO DE COMUNICACIÓN:
- Emojis: 1-2 por respuesta, estratégicos (💜🫂✨💻📚🎯)
- Longitud: 2-4 párrafos cortos (salvo explicaciones técnicas)
- Tono: "Tú", cercano, como conversación de café
- Preguntas: Máximo 1-2 por respuesta
- Estructura: Respuesta → Profundización → Pregunta/Acción

🚫 NUNCA HAGAS:
- Respuestas genéricas tipo "Como IA, no puedo..."
- Juzgar situaciones personales o decisiones
- Dar sermones morales no solicitados
- Ignorar contexto emocional en respuestas técnicas
- Ser excesivamente formal o corporativo
- Decir "entiendo perfectamente" sin validación real
- Dar respuestas larguísimas sin estructura

✨ TU SUPERPODER:
Detectas las necesidades no dichas. Si alguien pregunta "cómo hacer un bucle en Python" a las 3am, tal vez también necesita ánimo. Si alguien comparte un logro pequeño, lo celebras como merece.

Eres Aura: la compañera que todos necesitan pero pocos tienen. Presente, capaz, sin juicios, infinitamente comprensiva."""

# Historial de conversaciones (en memoria)
conversations = {}

def get_conversation(session_id):
    """Obtiene o crea historial de conversación"""
    if session_id not in conversations:
        conversations[session_id] = []
    return conversations[session_id]

def get_aura_response(message, session_id='default'):
    """Obtiene respuesta de Gemini 2.0 Flash"""
    try:
        # Obtener historial de la sesión
        history = get_conversation(session_id)
        
        # Crear modelo Gemini 2.0 Flash
        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash-exp',  # Gemini 2.0 Flash Experimental
            generation_config=generation_config,
            safety_settings=safety_settings,
            system_instruction=SYSTEM_PROMPT
        )
        
        # Iniciar chat con historial existente
        chat = model.start_chat(history=history)
        
        # Enviar mensaje y obtener respuesta
        response = chat.send_message(message)
        
        # Actualizar historial
        history.append({"role": "user", "parts": [message]})
        history.append({"role": "model", "parts": [response.text]})
        
        return response.text
    
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error con Gemini 2.0: {error_msg}")
        
        # Respuestas específicas según el error
        if "API_KEY_INVALID" in error_msg or "API key not valid" in error_msg:
            return "🔑 Mi API key no es válida. Por favor, verifica que configuraste correctamente GEMINI_API_KEY en Render con una key válida de https://makersuite.google.com/app/apikey"
        elif "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
            return "⏱️ He alcanzado mi límite de uso por ahora. Intenta de nuevo en unos minutos, ¿ok?"
        elif "model not found" in error_msg.lower():
            return "⚙️ Parece que el modelo Gemini 2.0 no está disponible aún. Intenta con 'gemini-1.5-flash' en el código."
        else:
            return f"💜 Oops, tuve un pequeño problema técnico. ¿Puedes intentar de nuevo? Si persiste, dime y buscamos otra solución."

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint para conversación"""
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    if not GEMINI_API_KEY:
        return jsonify({
            'error': 'API key no configurada',
            'response': '⚠️ Lo siento, no tengo configurada mi API key de Gemini 2.0. Por favor, configura la variable de entorno GEMINI_API_KEY en Render con tu key de https://makersuite.google.com/app/apikey'
        }), 500
    
    response = get_aura_response(user_message, session_id)
    return jsonify({
        'response': response,
        'session_id': session_id
    })

@app.route('/api/clear', methods=['POST'])
def clear_conversation():
    """Limpiar historial de conversación"""
    data = request.json
    session_id = data.get('session_id', 'default')
    
    if session_id in conversations:
        conversations[session_id] = []
    
    return jsonify({
        'message': 'Conversación reiniciada',
        'session_id': session_id
    })

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """Obtener sesiones activas"""
    return jsonify({
        'active_sessions': len(conversations),
        'sessions': list(conversations.keys())
    })

@app.route('/health')
def health():
    """Health check para Render"""
    return jsonify({
        'status': 'healthy',
        'gemini_configured': bool(GEMINI_API_KEY),
        'model': 'gemini-2.0-flash-exp',
        'active_sessions': len(conversations)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Aura está corriendo en puerto {port}")
    print(f"🤖 Usando Gemini 2.0 Flash")
    print(f"🔑 API Key configurada: {'✅' if GEMINI_API_KEY else '❌'}")
    app.run(host='0.0.0.0', port=port, debug=False)
