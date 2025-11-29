# Telegram AI Chatbot with Groq

AI-powered Telegram bot using Groq's free LLM API (llama-3.3-70b-versatile model).

## Features

- 🤖 AI-powered responses using Groq API
- 💬 Conversation memory (remembers context)
- ⚡ Fast responses with Groq's optimized inference
- 🔄 Auto-restart on crashes
- 📝 Simple commands (/start, /help, /clear)

## Setup

### Environment Variables

Set these in your deployment platform:

- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token from BotFather
- `GROQ_API_KEY` - Your Groq API key

### Local Development

```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="your-bot-token"
export GROQ_API_KEY="your-groq-api-key"
python main.py
```

## Commands

- `/start` - Start the bot and see welcome message
- `/help` - Show help message
- `/clear` - Clear conversation history

## Deployment

This bot is designed to run on Railway, Heroku, or any platform supporting Python workers.

Created by Abir 💙
