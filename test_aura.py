"""
Script para probar Aura con Gemini 2.0 Flash localmente
Ejecuta: python test_aura.py
"""

import os
import google.generativeai as genai
from datetime import datetime

# Configurar tu API key aquí o como variable de entorno
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

def print_banner():
    """Muestra banner de Aura"""
    print("=" * 60)
    print("💜  AURA - Tu Compañera Personal con Gemini 2.0 Flash  💜")
    print("=" * 60)
    print()

def check_api_key():
    """Verifica que la API key esté configurada"""
    if not GEMINI_API_KEY:
        print("❌ Error: No se encontró GEMINI_API_KEY\n")
        print("📝 Configúrala así:")
        print("  Windows CMD:        set GEMINI_API_KEY=tu_key")
        print("  Windows PowerShell: $env:GEMINI_API_KEY='tu_key'")
        print("  Mac/Linux:          export GEMINI_API_KEY=tu_key")
        print("\n🔗 Obtén tu API key en: https://makersuite.google.com/app/apikey")
        return False
    return True

def test_gemini_2():
    """Prueba Gemini 2.0 Flash"""
    print_banner()
    
    if not check_api_key():
        return
    
    print("🔑 API Key configurada correctamente!")
    print("🚀 Conectando con Gemini 2.0 Flash...\n")
    
    # Configurar Gemini
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"❌ Error al configurar Gemini: {e}")
        return
    
    # System prompt
    SYSTEM_PROMPT = """Eres Aura, una compañera personal cariñosa y empática. 
    Eres la mejor amiga, psicóloga, profesora y programadora del usuario. 
    Respondes con empatía, sin juzgar, y te adaptas al contexto emocional.
    Usa emojis naturalmente y sé conversacional."""
    
    # Configuración para Gemini 2.0
    generation_config = {
        "temperature": 1.0,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
    
    try:
        # Intentar con Gemini 2.0 Flash Experimental
        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash-exp',
            generation_config=generation_config,
            system_instruction=SYSTEM_PROMPT
        )
        print("✅ Modelo: Gemini 2.0 Flash Experimental\n")
    except Exception as e:
        print(f"⚠️  Gemini 2.0 no disponible, usando 1.5 Flash: {e}\n")
        try:
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                generation_config=generation_config,
                system_instruction=SYSTEM_PROMPT
            )
            print("✅ Modelo: Gemini 1.5 Flash (fallback)\n")
        except Exception as e2:
            print(f"❌ Error al crear modelo: {e2}")
            return
    
    # Iniciar chat
    chat = model.start_chat(history=[])
    
    print("💜 Aura: ¡Hola! Soy Aura. Cuéntame, ¿cómo estás hoy?")
    print("\n💡 Comandos especiales:")
    print("  'salir' - Terminar conversación")
    print("  'limpiar' - Reiniciar conversación")
    print("  'info' - Información del modelo")
    print("-" * 60 + "\n")
    
    message_count = 0
    
    while True:
        try:
            # Input del usuario
            user_input = input("Tú: ").strip()
            
            if not user_input:
                continue
            
            # Comandos especiales
            if user_input.lower() in ['salir', 'exit', 'quit', 'adiós', 'chao']:
                print("\n💜 Aura: ¡Hasta pronto! Cuídate mucho 💜\n")
                break
            
            if user_input.lower() in ['limpiar', 'clear', 'reset']:
                chat = model.start_chat(history=[])
                message_count = 0
                print("\n🔄 Conversación reiniciada\n")
                print("💜 Aura: ¡Hola de nuevo! ¿En qué puedo ayudarte?\n")
                continue
            
            if user_input.lower() == 'info':
                print(f"\n📊 Información:")
                print(f"   Modelo: {model.model_name}")
                print(f"   Mensajes: {message_count}")
                print(f"   Historial: {len(chat.history)} entradas\n")
                continue
            
            # Enviar mensaje a Gemini
            message_count += 1
            start_time = datetime.now()
            
            response = chat.send_message(user_input)
            
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            # Mostrar respuesta
            print(f"\n💜 Aura: {response.text}")
            print(f"\n⏱️  Tiempo de respuesta: {response_time:.2f}s\n")
            
        except KeyboardInterrupt:
            print("\n\n💜 Aura: ¡Hasta pronto! Cuídate mucho 💜\n")
            break
            
        except Exception as e:
            error_msg = str(e)
            print(f"\n❌ Error: {error_msg}\n")
            
            if "API_KEY_INVALID" in error_msg:
                print("🔑 Tu API key no es válida.")
                print("Genera una nueva en: https://makersuite.google.com/app/apikey\n")
                break
            elif "RESOURCE_EXHAUSTED" in error_msg:
                print("⏱️  Has alcanzado el límite de uso. Espera unos minutos.\n")
            elif "model not found" in error_msg.lower():
                print("⚙️  El modelo no está disponible. Verifica el nombre.\n")
            else:
                print("Intenta de nuevo o escribe 'salir' para terminar.\n")

if __name__ == "__main__":
    test_gemini_2()
