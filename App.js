import React, { useState, useRef, useEffect } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  StatusBar,
  ActivityIndicator
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '¡Hola! Soy Aura 💜 Estoy aquí para ti en cualquier rol que necesites: como tu mejor amiga, tu psicóloga, tu profesora, tu programadora... o simplemente para charlar. No hay juicios aquí, solo apoyo y comprensión. ¿En qué puedo ayudarte hoy?'
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const scrollViewRef = useRef();

  const getAuraResponse = (userMessage) => {
    const msg = userMessage.toLowerCase();
    
    if (msg.includes('triste') || msg.includes('deprimid') || msg.includes('mal')) {
      return '💜 Siento mucho que estés pasando por esto. Tus sentimientos son completamente válidos. No estás solo/a en esto. ¿Quieres contarme más sobre lo que está pasando? Estoy aquí para escucharte sin juzgar.';
    }
    
    if (msg.includes('ansiedad') || msg.includes('ansios') || msg.includes('nervios')) {
      return '🫂 La ansiedad puede ser muy abrumadora, pero respira conmigo. Vamos a tomarlo con calma. Intenta esto: inhala profundamente por 4 segundos, mantén por 4, exhala por 4. Repite. ¿Quieres que hablemos sobre qué está causando esta ansiedad?';
    }
    
    if (msg.includes('feliz') || msg.includes('genial') || msg.includes('bien')) {
      return '✨ ¡Me encanta escuchar eso! Tu alegría me alegra a mí también. Cuéntame más, ¿qué te tiene tan feliz?';
    }
    
    if (msg.includes('enseñ') || msg.includes('aprend') || msg.includes('explicar')) {
      return '📚 ¡Me encanta enseñar! Intentaré explicártelo de la manera más clara posible. No hay preguntas tontas aquí. ¿Sobre qué tema específico necesitas ayuda?';
    }
    
    if (msg.includes('código') || msg.includes('programar') || msg.includes('bug')) {
      return '💻 ¡Hablemos de código! Me encanta programar. Puedo ayudarte con debugging, explicarte conceptos, o revisar tu código. ¿Qué lenguaje estás usando y cuál es el desafío?';
    }
    
    if (msg.includes('gracias')) {
      return '💜 No tienes que agradecer. Para eso estoy aquí. ¿Hay algo más en lo que pueda ayudarte?';
    }
    
    if (msg.includes('hola') || msg.includes('hey')) {
      return '¡Hola! 😊 ¿Cómo estás hoy? ¿En qué puedo ayudarte?';
    }
    
    const responses = [
      '💜 Entiendo. Cuéntame más sobre eso. Estoy aquí para escucharte.',
      '✨ Interesante. ¿Qué más puedes contarme al respecto?',
      '🫂 Te escucho. No hay prisa, tómate tu tiempo.',
      '💭 Comprendo lo que dices. ¿Cómo te hace sentir eso?',
      '🌟 Estoy aquí contigo. ¿Quieres profundizar en eso?'
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    setTimeout(() => {
      const response = getAuraResponse(input);
      setMessages(prev => [...prev, { role: 'assistant', content: response }]);
      setIsTyping(false);
    }, 1000);
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" />
      <LinearGradient
        colors={['#4c1d95', '#312e81', '#1e3a8a']}
        style={styles.gradient}
      >
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.headerContent}>
            <Text style={styles.title}>Aura</Text>
            <View style={styles.onlineIndicator} />
          </View>
          <Text style={styles.subtitle}>
            Tu compañera de confianza • Sin juicios
          </Text>
          
          <View style={styles.rolesContainer}>
            <View style={styles.role}>
              <Text style={styles.roleText}>💜 Amiga</Text>
            </View>
            <View style={styles.role}>
              <Text style={styles.roleText}>🧠 Psicóloga</Text>
            </View>
            <View style={styles.role}>
              <Text style={styles.roleText}>📚 Profesora</Text>
            </View>
            <View style={styles.role}>
              <Text style={styles.roleText}>💻 Programadora</Text>
            </View>
          </View>
        </View>

        {/* Messages */}
        <ScrollView
          ref={scrollViewRef}
          style={styles.messagesContainer}
          contentContainerStyle={styles.messagesContent}
          onContentSizeChange={() => scrollViewRef.current.scrollToEnd()}
        >
          {messages.map((message, index) => (
            <View
              key={index}
              style={[
                styles.messageBubble,
                message.role === 'user' ? styles.userBubble : styles.assistantBubble
              ]}
            >
              <Text style={styles.messageText}>{message.content}</Text>
            </View>
          ))}
          
          {isTyping && (
            <View style={[styles.messageBubble, styles.assistantBubble]}>
              <View style={styles.typingIndicator}>
                <View style={styles.typingDot} />
                <View style={styles.typingDot} />
                <View style={styles.typingDot} />
              </View>
            </View>
          )}
        </ScrollView>

        {/* Input */}
        <KeyboardAvoidingView
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
        >
          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              value={input}
              onChangeText={setInput}
              placeholder="Escribe lo que sientes..."
              placeholderTextColor="rgba(216, 180, 254, 0.6)"
              multiline
            />
            <TouchableOpacity
              style={[styles.sendButton, !input.trim() && styles.sendButtonDisabled]}
              onPress={handleSend}
              disabled={!input.trim()}
            >
              <LinearGradient
                colors={['#a855f7', '#ec4899']}
                style={styles.sendButtonGradient}
              >
                <Text style={styles.sendButtonText}>➤</Text>
              </LinearGradient>
            </TouchableOpacity>
          </View>
        </KeyboardAvoidingView>
      </LinearGradient>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  gradient: {
    flex: 1,
  },
  header: {
    paddingTop: Platform.OS === 'ios' ? 50 : 40,
    paddingHorizontal: 20,
    paddingBottom: 20,
    backgroundColor: 'rgba(168, 85, 247, 0.2)',
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255, 255, 255, 0.1)',
  },
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: 'white',
  },
  onlineIndicator: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: '#4ade80',
  },
  subtitle: {
    fontSize: 13,
    color: 'rgba(216, 180, 254, 0.9)',
    marginTop: 4,
  },
  rolesContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginTop: 12,
  },
  role: {
    backgroundColor: 'rgba(168, 85, 247, 0.3)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  roleText: {
    color: 'white',
    fontSize: 11,
  },
  messagesContainer: {
    flex: 1,
  },
  messagesContent: {
    padding: 16,
    gap: 12,
  },
  messageBubble: {
    maxWidth: '80%',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 20,
  },
  userBubble: {
    alignSelf: 'flex-end',
    backgroundColor: '#a855f7',
  },
  assistantBubble: {
    alignSelf: 'flex-start',
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.2)',
  },
  messageText: {
    color: 'white',
    fontSize: 15,
    lineHeight: 22,
  },
  typingIndicator: {
    flexDirection: 'row',
    gap: 4,
  },
  typingDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#a855f7',
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 16,
    gap: 12,
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderTopWidth: 1,
    borderTopColor: 'rgba(255, 255, 255, 0.1)',
  },
  input: {
    flex: 1,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 12,
    color: 'white',
    fontSize: 15,
    maxHeight: 100,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.2)',
  },
  sendButton: {
    width: 50,
    height: 50,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendButtonDisabled: {
    opacity: 0.5,
  },
  sendButtonGradient: {
    width: 50,
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendButtonText: {
    color: 'white',
    fontSize: 20,
    fontWeight: 'bold',
  },
});
