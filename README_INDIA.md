# 🇮🇳 Conversational AI Voice Agent for India
## Hindi + English Support | 100% Open Source | Natural & Human-like

A production-ready voice agent specifically designed for Indian customers that communicates naturally in **Hindi**, **English**, and **Hinglish** (mixed language). Built entirely with open-source models.

---

## ✨ Key Features

- 🗣️ **Bilingual Support**: Automatically detects and responds in Hindi, English, or Hinglish
- 🤖 **Qwen2.5 Model**: State-of-the-art open-source LLM with excellent multilingual capabilities
- 🎤 **Voice Interaction**: Real-time speech-to-text and text-to-speech
- 💬 **Natural Conversations**: Contextual memory for human-like dialogues
- 🔒 **100% Open Source**: No API keys required, runs completely offline
- 🇮🇳 **India-Optimized**: Culturally aware responses for Indian context

---

## 🚀 Quick Start

### Step 1: Install Ollama

```bash
# Linux/Mac
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Download from https://ollama.ai/
```

### Step 2: Pull Qwen2.5 Model

```bash
# Recommended for most systems (good balance of speed and quality)
ollama pull qwen2.5:7b

# For slower systems (faster but less capable)
ollama pull qwen2.5:3b

# For powerful systems (best quality)
ollama pull qwen2.5:14b
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Agent

```bash
# Text mode (recommended for testing)
python voice_agent_india.py --mode text

# Voice mode (requires microphone)
python voice_agent_india.py --mode voice

# Show setup help
python voice_agent_india.py --setup
```

---

## 💡 Usage Examples

### Text Mode Conversation

```
🤖 Assistant: नमस्ते! मैं आपका AI सहायक हूँ। कैसे मदद करूँ?
   Hello! I'm your AI assistant. How can I help you today?

👤 You: Hello, I want to know about Diwali celebrations

🤖 Assistant: Diwali is one of the most important festivals in India! 
It's celebrated with lights, fireworks, family gatherings, and sweets. 
Would you like to know about specific traditions or regional variations?

👤 You: मुझे पता करना है कि इस साल दिवाली कब है

🤖 Assistant: 2024 में दिवाली 1 नवंबर को मनाई जाएगी। 
यह अमावस्या के दिन आती है और पांच दिनों तक चलती है। 
क्या आप दिवाली की तैयारियों के बारे में भी जानना चाहेंगे?

👤 You: Thank you! That's all I needed.

🤖 Assistant: धन्यवाद! आपका दिन शुभ हो! Have a great day!
```

### Voice Mode

Just speak naturally in Hindi or English:
- "Hello, how are you?" → Responds in English
- "नमस्ते, कैसे हो?" → Responds in Hindi  
- "Hi, mera naam Rahul hai" → Responds in Hinglish

---

## 🛠️ Configuration

Edit `config.yaml` to customize:

```yaml
local_qwen:
  model: "qwen2.5:7b"        # Model size (3b, 7b, 14b, 32b)
  temperature: 0.7            # Creativity level (0.1-1.0)
  max_tokens: 512             # Response length

speech_recognition:
  language: "hi"              # Default language
  phrase_time_limit: 20       # Max speech duration

conversation:
  max_history: 12             # Context memory size
  system_prompt: |            # Custom personality
    You are a friendly AI assistant for Indian customers...
```

---

## 📋 Requirements

- **Python**: 3.8+
- **Ollama**: Latest version
- **Model**: qwen2.5:7b (or other variants)
- **Microphone**: For voice mode
- **Speakers**: For audio output

### Python Dependencies

```txt
ollama>=0.1.0
PyYAML>=6.0
SpeechRecognition>=3.10.0
pyttsx3>=2.90
```

---

## 🌍 Language Capabilities

The agent seamlessly handles:

| Language | Script | Example |
|----------|--------|---------|
| Hindi | Devanagari | नमस्ते, कैसे हैं आप? |
| English | Latin | Hello, how are you? |
| Hinglish | Mixed | Hi, main theek hoon |

---

## 🔧 Troubleshooting

### "Model not found"
```bash
ollama pull qwen2.5:7b
ollama serve
```

### "No microphone detected"
- Check microphone permissions
- Test with: `arecord -l` (Linux) or System Preferences (Mac)

### "Speech not recognized"
- Speak clearly and at moderate pace
- Reduce background noise
- Try switching between Hindi/English

### Slow responses
- Use smaller model: `ollama pull qwen2.5:3b`
- Close other applications
- Ensure adequate RAM (8GB+ recommended)

---

## 📁 Project Structure

```
/workspace/
├── voice_agent_india.py    # Main agent code
├── config.yaml             # Configuration file
├── requirements.txt        # Python dependencies
├── README_INDIA.md         # This documentation
└── open_source_voice_agent/ # Additional resources
```

---

## 🎯 Use Cases

Perfect for:
- 🏦 **Customer Service**: Bank inquiries, support hotlines
- 🏥 **Healthcare**: Appointment booking, basic queries
- 🛒 **E-commerce**: Product information, order tracking
- 📚 **Education**: Tutoring, language learning
- 🏠 **Smart Home**: Voice-controlled automation
- 🚕 **Transportation**: Booking, route information

---

## 📝 License

This project uses 100% open-source components:
- **Qwen2.5**: Apache 2.0 License
- **Ollama**: MIT License
- **SpeechRecognition**: BSD License
- **pyttsx3**: LGPL License

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Better Hindi TTS voices
- Regional language support (Tamil, Telugu, Bengali, etc.)
- Integration with Indian services (UPI, Aadhaar verification, etc.)
- Custom domain knowledge for specific industries

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Run: `python voice_agent_india.py --setup`
3. Review logs in console output

---

**Built with ❤️ for India** | Powered by Qwen2.5 & Open Source
