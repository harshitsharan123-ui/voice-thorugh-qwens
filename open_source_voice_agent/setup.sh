#!/bin/bash

echo "🚀 Setting up Open Source Voice Agent..."
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version

# Install system dependencies based on OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "📦 Installing Linux system dependencies..."
    sudo apt-get update
    sudo apt-get install -y portaudio19-dev python3-pyaudio espeak espeak-data libespeak-dev ffmpeg
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "📦 Installing macOS system dependencies..."
    brew install portaudio espeak ffmpeg
else
    echo "⚠️  Unknown OS. Please install dependencies manually."
fi

# Install Python packages
echo "📦 Installing Python packages..."
pip install -r requirements.txt

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "📥 Ollama not found. Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "✅ Ollama already installed"
fi

# Pull Qwen model
echo "📥 Pulling Qwen2.5 7B model (this may take a few minutes)..."
ollama pull qwen2.5:7b

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Make sure your microphone is connected"
echo "   2. Run: python voice_agent.py --mode voice"
echo "   3. For better TTS quality, optionally install Coqui: pip install TTS"
echo ""
