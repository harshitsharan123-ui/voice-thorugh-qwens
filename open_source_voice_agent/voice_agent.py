#!/usr/bin/env python3
"""
Open Source Conversational AI Voice Agent
Uses 100% open-source models: Qwen2.5 (LLM), Whisper (STT), Coqui/pyttsx3 (TTS)
"""

import argparse
import sys
import os
from typing import List, Optional
import json

# Import speech recognition
try:
    import speech_recognition as sr
except ImportError:
    print("Please install speech_recognition: pip install speechrecognition")
    sys.exit(1)

# Import Whisper for better STT (optional fallback to Google)
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("Whisper not installed. Using Google Speech API as fallback.")

# Import TTS engines
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    from TTS.api import TTS
    COQUI_AVAILABLE = True
except ImportError:
    COQUI_AVAILABLE = False

# Import Ollama for Qwen
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("Please install ollama: pip install ollama")
    sys.exit(1)


class ConversationMemory:
    """Maintains conversation context for natural dialogue"""
    
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.history: List[dict] = []
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation history"""
        self.history.append({"role": role, "content": content})
        # Keep only recent messages
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_context(self) -> List[dict]:
        """Get conversation history for LLM context"""
        return self.history
    
    def clear(self):
        """Clear conversation history"""
        self.history = []


class VoiceAgent:
    """Main voice agent class with STT, LLM, and TTS capabilities"""
    
    def __init__(
        self,
        model: str = "qwen2.5:7b",
        temperature: float = 0.7,
        tts_engine: str = "pyttsx3",
        voice: Optional[str] = None,
        use_whisper: bool = True
    ):
        self.model = model
        self.temperature = temperature
        self.tts_engine = tts_engine
        self.use_whisper = use_whisper and WHISPER_AVAILABLE
        
        # Initialize conversation memory
        self.memory = ConversationMemory()
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            print("🎤 Calibrating microphone for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Microphone calibrated!")
        
        # Initialize Whisper model if available
        if self.use_whisper:
            print("🧠 Loading Whisper model (this may take a moment)...")
            self.whisper_model = whisper.load_model("base")
            print("✅ Whisper loaded!")
        else:
            self.whisper_model = None
        
        # Initialize TTS engine
        self._init_tts(tts_engine, voice)
        
        # System prompt for natural conversation
        self.system_prompt = """You are a friendly, helpful, and natural conversational AI assistant. 
Your responses should be:
- Conversational and human-like (use contractions, natural phrasing)
- Concise but informative (avoid overly long responses)
- Empathetic and engaging
- Context-aware (remember previous parts of the conversation)

Speak naturally as if you're having a real conversation with a friend."""
    
    def _init_tts(self, engine: str, voice: Optional[str] = None):
        """Initialize text-to-speech engine"""
        if engine == "coqui" and COQUI_AVAILABLE:
            print("🔊 Initializing Coqui TTS...")
            model_name = voice or "tts_models/en/ljspeech/tacotron2-DDC"
            self.tts = TTS(model_name=model_name)
            self.tts_engine = "coqui"
            print("✅ Coqui TTS ready!")
        elif PYTTSX3_AVAILABLE:
            print("🔊 Initializing pyttsx3...")
            self.engine = pyttsx3.init()
            
            # Configure voice properties
            voices = self.engine.getProperty('voices')
            if voice:
                # Try to find specified voice
                for v in voices:
                    if voice.lower() in v.name.lower():
                        self.engine.setProperty('voice', v.id)
                        break
            else:
                # Use female voice if available (often sounds more natural)
                if len(voices) > 1:
                    self.engine.setProperty('voice', voices[1].id)
            
            # Set speech rate and volume
            self.engine.setProperty('rate', 175)  # Slightly faster for natural flow
            self.engine.setProperty('volume', 0.9)
            
            self.tts_engine = "pyttsx3"
            print("✅ pyttsx3 ready!")
        else:
            raise RuntimeError("No TTS engine available. Install pyttsx3 or TTS (Coqui)")
    
    def listen(self) -> Optional[str]:
        """Listen to microphone and convert speech to text"""
        try:
            with self.microphone as source:
                print("👂 Listening... (speak now)")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("🔄 Processing speech...")
            
            # Use Whisper if available, otherwise fall back to Google
            if self.use_whisper and self.whisper_model:
                # Save audio to temporary file
                import tempfile
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                    temp_path = f.name
                    f.write(audio.get_wav_data())
                
                try:
                    result = self.whisper_model.transcribe(temp_path)
                    text = result["text"].strip()
                finally:
                    os.unlink(temp_path)
            else:
                # Fallback to Google Speech Recognition
                text = self.recognizer.recognize_google(audio)
            
            if text:
                print(f"🗣️ You said: '{text}'")
                return text
            else:
                print("❌ No speech detected. Please try again.")
                return None
                
        except sr.WaitTimeoutError:
            print("⏰ Timeout: No speech detected")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def think(self, user_input: str) -> str:
        """Generate response using Qwen via Ollama"""
        # Add user message to memory
        self.memory.add_message("user", user_input)
        
        # Build messages with system prompt
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.memory.get_context()
        ]
        
        try:
            print("🤔 Thinking...")
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": self.temperature,
                    "top_p": 0.9,
                }
            )
            
            assistant_response = response["message"]["content"].strip()
            
            # Add assistant response to memory
            self.memory.add_message("assistant", assistant_response)
            
            print(f"🤖 Agent: '{assistant_response}'")
            return assistant_response
            
        except Exception as e:
            error_msg = f"I'm sorry, I encountered an error: {str(e)}"
            print(f"❌ Error generating response: {e}")
            return error_msg
    
    def speak(self, text: str):
        """Convert text to speech and play it"""
        if not text:
            return
        
        try:
            if self.tts_engine == "coqui":
                # Coqui TTS
                self.tts.tts_to_file(text=text, file_path="output.wav")
                # Play the audio file
                import subprocess
                subprocess.call(["aplay", "output.wav"])  # Linux
                # For macOS: subprocess.call(["afplay", "output.wav"])
                os.remove("output.wav")
            else:
                # pyttsx3
                self.engine.say(text)
                self.engine.runAndWait()
                
        except Exception as e:
            print(f"❌ TTS error: {e}")
            # Fallback: just print the response
            print(f"Response: {text}")
    
    def chat(self, user_input: str) -> str:
        """Process user input and generate spoken response"""
        response = self.think(user_input)
        self.speak(response)
        return response
    
    def interactive_mode(self):
        """Run interactive voice conversation"""
        print("\n" + "="*60)
        print("🎙️  Voice Agent Ready! (Press Ctrl+C to exit)")
        print("="*60)
        print("Commands:")
        print("  - Just speak naturally")
        print("  - Say 'clear' to reset conversation memory")
        print("  - Say 'quit' or 'exit' to stop")
        print("="*60 + "\n")
        
        # Greet user
        greeting = "Hello! I'm your AI assistant. How can I help you today?"
        print(f"🤖 Agent: '{greeting}'")
        self.speak(greeting)
        
        try:
            while True:
                user_input = self.listen()
                
                if user_input:
                    user_lower = user_input.lower().strip()
                    
                    # Check for commands
                    if user_lower in ["quit", "exit", "bye", "goodbye"]:
                        farewell = "Goodbye! Have a great day!"
                        print(f"🤖 Agent: '{farewell}'")
                        self.speak(farewell)
                        break
                    elif user_lower == "clear":
                        self.memory.clear()
                        confirmation = "Conversation memory cleared!"
                        print(f"🤖 Agent: '{confirmation}'")
                        self.speak(confirmation)
                        continue
                    
                    # Process normal conversation
                    self.chat(user_input)
                    
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            farewell = "Goodbye! It was nice chatting with you."
            self.speak(farewell)
    
    def text_mode(self):
        """Run text-based conversation (no voice)"""
        print("\n" + "="*60)
        print("💬 Text Mode Active (Type 'quit' to exit)")
        print("="*60 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                user_lower = user_input.lower()
                
                if user_lower in ["quit", "exit"]:
                    print("🤖 Agent: Goodbye!")
                    break
                elif user_lower == "clear":
                    self.memory.clear()
                    print("🤖 Agent: Conversation memory cleared!")
                    continue
                
                # Generate and display response (no speech)
                response = self.think(user_input)
                print(f"🤖 Agent: {response}\n")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                break


def main():
    parser = argparse.ArgumentParser(
        description="Open Source Conversational AI Voice Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python voice_agent.py --mode voice
  python voice_agent.py --mode text
  python voice_agent.py --model qwen2.5:14b --temperature 0.8
  python voice_agent.py --tts-engine coqui --voice en_US-lessac-medium
        """
    )
    
    parser.add_argument(
        "--mode",
        choices=["voice", "text"],
        default="voice",
        help="Interaction mode: voice (default) or text"
    )
    
    parser.add_argument(
        "--model",
        default="qwen2.5:7b",
        help="Ollama model to use (default: qwen2.5:7b)"
    )
    
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Response creativity (0.0-1.0, default: 0.7)"
    )
    
    parser.add_argument(
        "--tts-engine",
        choices=["pyttsx3", "coqui"],
        default="pyttsx3",
        help="Text-to-speech engine (default: pyttsx3)"
    )
    
    parser.add_argument(
        "--voice",
        type=str,
        default=None,
        help="Voice ID/name for TTS"
    )
    
    parser.add_argument(
        "--no-whisper",
        action="store_true",
        help="Disable Whisper and use Google Speech API"
    )
    
    args = parser.parse_args()
    
    # Check dependencies
    if not OLLAMA_AVAILABLE:
        print("❌ Error: ollama package not installed")
        print("Install with: pip install ollama")
        sys.exit(1)
    
    if args.mode == "voice" and not PYTTSX3_AVAILABLE and not COQUI_AVAILABLE:
        print("❌ Error: No TTS engine available")
        print("Install with: pip install pyttsx3")
        sys.exit(1)
    
    # Create and run agent
    try:
        agent = VoiceAgent(
            model=args.model,
            temperature=args.temperature,
            tts_engine=args.tts_engine,
            voice=args.voice,
            use_whisper=not args.no_whisper
        )
        
        if args.mode == "voice":
            agent.interactive_mode()
        else:
            agent.text_mode()
            
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
