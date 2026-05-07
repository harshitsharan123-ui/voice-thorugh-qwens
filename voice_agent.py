#!/usr/bin/env python3
"""
Conversational AI Voice Agent using Qwen LLM
Natural, human-like voice interactions with real-time speech processing
"""

import os
import sys
import json
import yaml
import logging
from typing import List, Dict, Optional
from datetime import datetime
import threading
import queue

# Import speech recognition
try:
    import speech_recognition as sr
except ImportError:
    print("Installing speech_recognition...")
    os.system("pip install SpeechRecognition")
    import speech_recognition as sr

# Import TTS
try:
    import pyttsx3
except ImportError:
    print("Installing pyttsx3...")
    os.system("pip install pyttsx3")
    import pyttsx3

# Import Qwen/DashScope
try:
    import dashscope
    from dashscope import Generation
except ImportError:
    print("Installing dashscope...")
    os.system("pip install dashscope")
    import dashscope
    from dashscope import Generation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ConversationManager:
    """Manages conversation history and context"""
    
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.history: List[Dict[str, str]] = []
        
    def add_message(self, role: str, content: str):
        """Add a message to conversation history"""
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Trim history if too long
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_context(self) -> List[Dict[str, str]]:
        """Get conversation context for LLM"""
        return self.history.copy()
    
    def clear(self):
        """Clear conversation history"""
        self.history = []
        logger.info("Conversation history cleared")


class SpeechRecognizer:
    """Handles speech-to-text conversion"""
    
    def __init__(self, language: str = "en-US", energy_threshold: int = 300):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.dynamic_energy_threshold = True
        self.language = language
        self.is_listening = False
        
    def listen_from_microphone(self, timeout: int = 5, phrase_time_limit: int = 15) -> Optional[str]:
        """Listen to microphone and convert speech to text"""
        try:
            with sr.Microphone() as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Listening...")
                
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                logger.info("Processing speech...")
                text = self.recognizer.recognize_google(audio, language=self.language)
                logger.info(f"Recognized: {text}")
                return text
                
        except sr.WaitTimeoutError:
            logger.warning("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error during speech recognition: {e}")
            return None
    
    def listen_from_audio_file(self, file_path: str) -> Optional[str]:
        """Convert audio file to text"""
        try:
            with sr.AudioFile(file_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio, language=self.language)
                logger.info(f"Recognized from file: {text}")
                return text
        except Exception as e:
            logger.error(f"Error processing audio file: {e}")
            return None


class TextToSpeech:
    """Handles text-to-speech conversion"""
    
    def __init__(self, rate: int = 150, pitch: int = 50, voice_id: Optional[str] = None):
        self.engine = pyttsx3.init()
        
        # Configure voice properties
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('pitch', pitch)
        
        # Set voice if specified
        if voice_id:
            self.engine.setProperty('voice', voice_id)
        else:
            # Use default female voice if available
            voices = self.engine.getProperty('voices')
            if len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)  # Usually female voice
        
        self.is_speaking = False
        self._stop_flag = False
        
    def speak(self, text: str, block: bool = True):
        """Convert text to speech and speak it"""
        try:
            logger.info(f"Speaking: {text}")
            self.is_speaking = True
            self._stop_flag = False
            
            if block:
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                # Non-blocking mode
                def _speak_thread():
                    self.engine.say(text)
                    self.engine.runAndWait()
                    self.is_speaking = False
                
                thread = threading.Thread(target=_speak_thread)
                thread.daemon = True
                thread.start()
            
            if not block:
                self.is_speaking = False
                
        except Exception as e:
            logger.error(f"TTS error: {e}")
            self.is_speaking = False
    
    def stop(self):
        """Stop current speech"""
        self._stop_flag = True
        try:
            self.engine.stop()
        except:
            pass
        self.is_speaking = False
    
    def list_voices(self):
        """List available voices"""
        voices = self.engine.getProperty('voices')
        logger.info("Available voices:")
        for i, voice in enumerate(voices):
            logger.info(f"  {i}: {voice.name} ({voice.id})")
        return voices


class QwenLLM:
    """Interfaces with Qwen LLM via DashScope API"""
    
    def __init__(self, api_key: str, model: str = "qwen-turbo"):
        dashscope.api_key = api_key
        self.model = model
        logger.info(f"Initialized Qwen LLM with model: {model}")
        
    def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 512,
        top_p: float = 0.9
    ) -> Optional[str]:
        """Generate response from Qwen LLM"""
        try:
            logger.info("Generating response from Qwen...")
            
            response = Generation.call(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                result_format='message'
            )
            
            if response.status_code == 200:
                content = response.output.choices[0].message.content
                logger.info(f"Qwen response: {content[:100]}...")
                return content
            else:
                logger.error(f"Qwen API error: {response.code} - {response.message}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling Qwen API: {e}")
            return None
    
    def generate_streaming(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 512
    ):
        """Generate streaming response from Qwen LLM"""
        try:
            responses = Generation.call(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                result_format='message'
            )
            
            for response in responses:
                if response.status_code == 200:
                    yield response.output.choices[0].message.content
                else:
                    logger.error(f"Streaming error: {response.message}")
                    
        except Exception as e:
            logger.error(f"Streaming error: {e}")


class VoiceAgent:
    """Main voice agent orchestrating all components"""
    
    def __init__(self, config_path: str = "config.yaml"):
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.conversation_manager = ConversationManager(
            max_history=self.config['conversation']['max_history']
        )
        
        self.speech_recognizer = SpeechRecognizer(
            language=self.config['speech_recognition']['language'],
            energy_threshold=self.config['speech_recognition']['energy_threshold']
        )
        
        self.tts = TextToSpeech(
            rate=self.config['voice']['speech_rate'],
            pitch=self.config['voice']['pitch'],
            voice_id=self.config['voice'].get('voice_id')
        )
        
        # Initialize Qwen LLM
        api_key = os.getenv('DASHSCOPE_API_KEY') or self.config['qwen']['api_key']
        if not api_key or api_key == "${DASHSCOPE_API_KEY}":
            logger.error("Please set DASHSCOPE_API_KEY environment variable")
            raise ValueError("DASHSCOPE_API_KEY not found")
        
        self.llm = QwenLLM(
            api_key=api_key,
            model=self.config['qwen']['model']
        )
        
        # Build system prompt
        self.system_prompt = self.config['conversation']['system_prompt']
        
        logger.info("Voice Agent initialized successfully")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {config_path}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Return default configuration"""
        return {
            'qwen': {
                'model': 'qwen-turbo',
                'max_tokens': 512,
                'temperature': 0.7,
                'top_p': 0.9
            },
            'voice': {
                'speech_rate': 150,
                'pitch': 50
            },
            'speech_recognition': {
                'language': 'en-US',
                'energy_threshold': 300
            },
            'conversation': {
                'max_history': 10,
                'system_prompt': "You are a friendly, helpful AI assistant."
            }
        }
    
    def process_user_input(self, user_text: str) -> str:
        """Process user input and generate AI response"""
        # Add user message to history
        self.conversation_manager.add_message("user", user_text)
        
        # Build messages for LLM
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_manager.get_context())
        
        # Generate response
        response = self.llm.generate_response(
            messages=messages,
            temperature=self.config['qwen']['temperature'],
            max_tokens=self.config['qwen']['max_tokens'],
            top_p=self.config['qwen']['top_p']
        )
        
        if response:
            # Add assistant response to history
            self.conversation_manager.add_message("assistant", response)
            return response
        else:
            error_msg = "I apologize, but I'm having trouble processing that right now. Could you try again?"
            self.conversation_manager.add_message("assistant", error_msg)
            return error_msg
    
    def run_interactive(self):
        """Run interactive voice conversation loop"""
        logger.info("=" * 60)
        logger.info("🎤 Voice Agent Started - Speak naturally!")
        logger.info("Say 'quit' or 'exit' to end the conversation")
        logger.info("=" * 60)
        
        # Greet user
        greeting = "Hello! I'm your AI assistant. How can I help you today?"
        logger.info(greeting)
        self.tts.speak(greeting)
        
        while True:
            try:
                # Listen for user speech
                user_text = self.speech_recognizer.listen_from_microphone(
                    timeout=10,
                    phrase_time_limit=self.config['speech_recognition']['phrase_time_limit']
                )
                
                if not user_text:
                    continue
                
                # Check for exit commands
                if user_text.lower() in ['quit', 'exit', 'goodbye', 'bye']:
                    farewell = "Goodbye! Have a great day!"
                    logger.info(farewell)
                    self.tts.speak(farewell)
                    break
                
                # Process and respond
                response = self.process_user_input(user_text)
                
                # Speak response
                self.tts.speak(response)
                
            except KeyboardInterrupt:
                logger.info("\nInterrupted by user")
                farewell = "Goodbye!"
                self.tts.speak(farewell)
                break
            except Exception as e:
                logger.error(f"Error in conversation loop: {e}")
                error_msg = "I encountered an error. Let's try again."
                self.tts.speak(error_msg)
    
    def run_text_mode(self):
        """Run in text-only mode (no voice)"""
        logger.info("=" * 60)
        logger.info("💬 Text Mode - Type your messages")
        logger.info("Type 'quit' or 'exit' to end")
        logger.info("=" * 60)
        
        print("\nAssistant: Hello! I'm your AI assistant. How can I help you today?\n")
        
        while True:
            try:
                user_text = input("You: ").strip()
                
                if not user_text:
                    continue
                
                if user_text.lower() in ['quit', 'exit', 'goodbye', 'bye']:
                    print("\nAssistant: Goodbye! Have a great day!\n")
                    break
                
                response = self.process_user_input(user_text)
                print(f"\nAssistant: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nAssistant: Goodbye!\n")
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                print("\nAssistant: I encountered an error. Let's try again.\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Conversational AI Voice Agent with Qwen')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to config file')
    parser.add_argument('--mode', type=str, choices=['voice', 'text'], default='voice', 
                       help='Run mode: voice or text')
    parser.add_argument('--list-voices', action='store_true', help='List available TTS voices')
    
    args = parser.parse_args()
    
    try:
        # Initialize agent
        agent = VoiceAgent(config_path=args.config)
        
        # List voices if requested
        if args.list_voices:
            agent.tts.list_voices()
            return
        
        # Run in specified mode
        if args.mode == 'voice':
            agent.run_interactive()
        else:
            agent.run_text_mode()
            
    except ValueError as e:
        logger.error(str(e))
        logger.error("\nTo get started:")
        logger.error("1. Get your API key from https://dashscope.console.aliyun.com/")
        logger.error("2. Set environment variable: export DASHSCOPE_API_KEY='your-key'")
        logger.error("3. Run the agent again\n")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
