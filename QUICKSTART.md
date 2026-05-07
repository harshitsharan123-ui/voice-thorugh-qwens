# Quick Start Guide

## Getting Your API Key (For Cloud Version)

1. Visit [DashScope Console](https://dashscope.console.aliyun.com/)
2. Sign up or log in to your Alibaba Cloud account
3. Create a new API key
4. Copy your API key
5. Set it as an environment variable:
   ```bash
   export DASHSCOPE_API_KEY="your-api-key-here"
   ```

## Installation

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Install PyAudio (if needed)

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

## Running the Voice Agent

### Option 1: Cloud-based (Recommended for beginners)

```bash
# Make sure you've set your API key
export DASHSCOPE_API_KEY="your-api-key-here"

# Run in voice mode (uses microphone and speakers)
python voice_agent.py --mode voice

# Run in text mode (keyboard input only)
python voice_agent.py --mode text

# List available voices
python voice_agent.py --list-voices
```

### Option 2: Local (Requires Ollama)

1. **Install Ollama:**
   - Visit [https://ollama.ai/](https://ollama.ai/)
   - Download and install for your OS

2. **Pull Qwen Model:**
   ```bash
   ollama pull qwen2.5:7b
   ```

3. **Start Ollama Server:**
   ```bash
   ollama serve
   ```

4. **Run Local Voice Agent:**
   ```bash
   python voice_agent_local.py --mode voice
   ```

## Configuration

Edit `config.yaml` to customize:

### Voice Settings
```yaml
voice:
  speech_rate: 150      # Words per minute (100-200 recommended)
  pitch: 50            # Pitch (0-100)
```

### Conversation Personality
```yaml
conversation:
  system_prompt: |
    You are a friendly, helpful AI assistant.
    Speak naturally with contractions and warmth.
  max_history: 10      # Messages to remember
```

### Qwen Model Settings
```yaml
qwen:
  model: "qwen-turbo"     # Options: qwen-turbo, qwen-plus, qwen-max
  temperature: 0.7        # Creativity (0.0-1.0)
  max_tokens: 512         # Response length
```

## Usage Examples

### Voice Mode
1. Run: `python voice_agent.py --mode voice`
2. Wait for the greeting
3. Speak naturally when prompted
4. Say "quit", "exit", or "goodbye" to end

### Text Mode
1. Run: `python voice_agent.py --mode text`
2. Type your messages
3. Press Enter to send
4. Type "quit" to end

## Troubleshooting

### No Audio Input/Output
- Check microphone permissions in your OS settings
- Ensure audio devices are properly connected
- Test with: `arecord -l` (Linux) or check Sound settings (macOS/Windows)

### API Errors
- Verify your API key is correct
- Check internet connection
- Ensure you have API credits remaining

### Slow Responses
- Try using `qwen-turbo` instead of `qwen-max`
- Reduce `max_tokens` in config
- For local version, use a smaller model

### Speech Recognition Issues
- Speak clearly and at moderate pace
- Reduce background noise
- Adjust `energy_threshold` in config if needed

## Advanced Usage

### Custom System Prompt
Create a custom personality in `config.yaml`:

```yaml
conversation:
  system_prompt: |
    You are a witty, knowledgeable assistant who loves science.
    Use humor when appropriate but stay accurate.
    Keep responses concise and engaging.
```

### Different Languages
Change the recognition language:

```yaml
speech_recognition:
  language: "es-ES"  # Spanish
  # or "fr-FR" for French, "de-DE" for German, etc.
```

### Streaming Responses
Enable real-time streaming (advanced):

```yaml
advanced:
  enable_streaming: true
```

## Performance Tips

1. **For fastest responses:** Use `qwen-turbo` model
2. **For best quality:** Use `qwen-max` model  
3. **For privacy:** Use local version with Ollama
4. **For offline use:** Local version only (requires downloaded model)

## Next Steps

- Customize the system prompt for your use case
- Integrate with other services (calendar, email, etc.)
- Deploy as a service or web application
- Add custom wake word detection
- Implement multi-user support

Enjoy your natural, human-like AI voice agent! 🎉
