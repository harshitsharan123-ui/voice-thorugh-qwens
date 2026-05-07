# Open Source Conversational AI Voice Agent

A natural, human-like voice agent using **100% open-source models** (Qwen + OpenAI Whisper + Coqui TTS).

## Features
- 🎙️ **Speech-to-Text**: OpenAI Whisper (open-source)
- 🧠 **LLM**: Qwen2.5 (open-source, runs locally via Ollama)
- 🔊 **Text-to-Speech**: Coqui TTS or pyttsx3 (open-source)
- 💾 **Conversation Memory**: Context-aware responses
- 🚀 **Fully Offline**: No API keys required

## Installation

### 1. Install System Dependencies
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -p portaudio19-dev python3-pyaudio espeak espeak-data libespeak-dev

# macOS
brew install portaudio espeak
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Ollama (for running Qwen locally)
```bash
# Linux/macOS
curl -fsSL https://ollama.com/install.sh | sh

# Pull Qwen2.5 model
ollama pull qwen2.5:7b
```

### 4. (Optional) Install Coqui TTS for better voice quality
```bash
pip install TTS
```

## Usage

### Voice Mode (Interactive)
```bash
python voice_agent.py --mode voice
```

### Text Mode (Terminal chat)
```bash
python voice_agent.py --mode text
```

### Customization
```bash
# Use different Qwen model size
ollama pull qwen2.5:14b
python voice_agent.py --model qwen2.5:14b

# Adjust response creativity (0.0-1.0)
python voice_agent.py --temperature 0.7

# Use Coqui TTS for more natural voice
python voice_agent.py --tts-engine coqui
```

## How It Works

1. **Listen**: Captures your voice via microphone
2. **Transcribe**: Converts speech to text using Whisper
3. **Think**: Qwen generates human-like response with context
4. **Speak**: Converts response back to natural speech

## Models Used

| Component | Model | License |
|-----------|-------|---------|
| Speech-to-Text | OpenAI Whisper | MIT |
| LLM | Qwen2.5 | Apache 2.0 |
| Text-to-Speech | Coqui TTS / pyttsx3 | MPL 2.0 / MIT |

## Troubleshooting

### Microphone Issues
```bash
# List available audio devices
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

### Slow Response Times
- Use smaller Qwen model: `ollama pull qwen2.5:3b`
- Reduce temperature: `--temperature 0.5`

### TTS Voice Quality
- Install Coqui TTS for neural voices
- Try different voices: `python voice_agent.py --voice en_US-lessac-medium`
