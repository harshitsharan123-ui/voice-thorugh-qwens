# Optional: Advanced configuration for power users

# Use larger Qwen model for better quality (requires more RAM)
# ollama pull qwen2.5:14b
# python voice_agent.py --model qwen2.5:14b

# Use smaller model for faster response on limited hardware
# ollama pull qwen2.5:3b
# python voice_agent.py --model qwen2.5:3b

# Enable Coqui TTS for more natural neural voices
# pip install TTS
# python voice_agent.py --tts-engine coqui --voice en_US-lessac-medium

# Adjust creativity level
# Higher temperature (0.8-0.9) = more creative, varied responses
# Lower temperature (0.3-0.5) = more focused, deterministic responses
# python voice_agent.py --temperature 0.8

# List available voices for pyttsx3
# python -c "import pyttsx3; engine = pyttsx3.init(); [print(v.name) for v in engine.getProperty('voices')]"

# Test microphone
# python -c "import speech_recognition as sr; r = sr.Recognizer(); m = sr.Microphone(); print(m.list_microphone_names())"

# Run in text-only mode (no voice I/O)
# python voice_agent.py --mode text

# Disable Whisper and use Google Speech API (requires internet)
# python voice_agent.py --no-whisper
