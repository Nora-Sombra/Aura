from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Respuestas de Aura
def get_aura_response(user_message):
    msg = user_message.lower()
    
    # Detección emocional
    if any(word in msg for word in ['triste', 'deprimid', 'mal', 'llorar', 'dolor']):
        return '💜 Siento mucho que estés pasando por esto. Tus sentimientos son completamente válidos. No estás solo/a en esto. ¿Quieres contarme más sobre lo que está pasando? Estoy aquí para escucharte sin juzgar.'
    
    if any(word in msg for word in ['ansiedad', 'ansios', 'nervios', 'estrés', 'pánico']):
        return '🫂 La ansiedad puede ser muy abrumadora, pero respira conmigo. Vamos a tomarlo con calma. Intenta esto: inhala profundamente por 4 segundos, mantén por 4, exhala por 4. Repite. ¿Quieres que hablemos sobre qué está causando esta ansiedad?'
    
    if any(word in msg for word in ['feliz', 'genial', 'bien', 'alegre', 'contento']):
        return '✨ ¡Me encanta escuchar eso! Tu alegría me alegra a mí también. Cuéntame más, ¿qué te tiene tan feliz?'
    
    # Aprendizaje
    if any(word in msg for word in ['enseñ', 'aprend', 'explicar', 'cómo', 'qué es']):
        return '📚 ¡Me encanta enseñar! Intentaré explicártelo de la manera más clara posible. No hay preguntas tontas aquí. Si algo no queda claro, pregúntame de nuevo de otra forma. ¿Sobre qué tema específico necesitas ayuda?'
    
    # Programación
    if any(word in msg for word in ['código', 'programar', 'bug', 'error', 'python', 'javascript', 'html', 'css']):
        return '💻 ¡Hablemos de código! Me encanta programar. Puedo ayudarte con debugging, explicarte conceptos, o revisar tu código. ¿Qué lenguaje estás usando y cuál es el desafío?'
    
    # Amistad
    if any(word in msg for word in ['amiga', 'charlar', 'aburr', 'solo', 'compañía']):
        return '☕ Aquí estoy para ti, como tu amiga. Podemos charlar de lo que quieras. ¿Qué hay en tu mente? ¿Cómo ha sido tu día?'
    
    # Agradecimientos
    if any(word in msg for word in ['gracias', 'thank']):
        return '💜 No tienes que agradecer. Para eso estoy aquí. ¿Hay algo más en lo que pueda ayudarte?'
    
    # Saludos
    if any(word in msg for word in ['hola', 'hey', 'qué tal', 'buenas']):
        return '¡Hola! 😊 ¿Cómo estás hoy? ¿En qué puedo ayudarte? Ya sea que necesites hablar, aprender algo nuevo, resolver un problema de código, o simplemente compañía.'
    
    # Respuesta empática por defecto
    responses = [
        '💜 Entiendo. Cuéntame más sobre eso. Estoy aquí para escucharte.',
        '✨ Interesante. ¿Qué más puedes contarme al respecto?',
        '🫂 Te escucho. No hay prisa, tómate tu tiempo.',
        '💭 Comprendo lo que dices. ¿Cómo te hace sentir eso?',
        '🌟 Estoy aquí contigo. ¿Quieres profundizar en eso?'
    ]
    
    import random
    return random.choice(responses)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    response = get_aura_response(user_message)
    return jsonify({'response': response})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
