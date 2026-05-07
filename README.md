# Conversational AI Voice Agent with Qwen

A natural, human-like voice agent powered by Qwen LLM with real-time speech interaction.

## Features
- 🎤 Real-time speech-to-text using Web Speech API or Whisper
- 🧠 Qwen LLM for natural conversations
- 🔊 High-quality text-to-speech with natural voices
- 💬 Context-aware conversations with memory
- 🚀 Low-latency responses for natural flow

## Prerequisites

```bash
pip install -r requirements.txt
```

## Quick Start

### Option 1: Using Qwen API (Recommended)
```bash
export DASHSCOPE_API_KEY="your-api-key"
python voice_agent.py
```

### Option 2: Using Local Qwen Model
```bash
python voice_agent_local.py
```

## Configuration

Edit `config.yaml` to customize:
- Voice settings (speed, pitch, voice type)
- Qwen model parameters
- Conversation personality
- Audio settings

## Usage

Run the agent:
```bash
python voice_agent.py
```

The agent will:
1. Listen for your speech
2. Process with Qwen LLM
3. Respond with natural voice
4. Maintain conversation context

## Advanced Features

- **Memory**: Remembers conversation history
- **Personality**: Customizable response style
- **Multi-language**: Supports multiple languages
- **Streaming**: Real-time audio streaming

## Requirements

See `requirements.txt` for dependencies.

## License

MIT License