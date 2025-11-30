import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

from start_banner import register_start_handlers

app = Application.builder().token(TOKEN).build()
# register other handlers...
register_start_handlers(app)
app.run_polling()

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Groq client
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Store conversation history per user
conversation_history = {}

# System prompt with developer information
SYSTEM_PROMPT = """You are a helpful AI assistant created Developed by Abir.So, Your developer is Abir, who created you using her curious mind. 
You are friendly, helpful, and remember that Abir is your creator. When Abir talks to you, acknowledge him as your developer.
Keep responses concise and helpful."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hi {user.first_name}! 👋\n\n"
        f"I'm an AI assistant Developed by Abir. Who created me using her curious mind. So, respect her work\n"
        f"Ask me anything and I'll do my best to help!\n\n"
        f"Commands:\n"
        f"/start - Start the bot\n"
        f"/clear - Clear conversation history\n"
        f"/help - Show this message"
    )

async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear conversation history for the user."""
    user_id = update.effective_user.id
    if user_id in conversation_history:
        conversation_history[user_id] = []
    await update.message.reply_text("✅ Conversation history cleared!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "AI Chatbot Help\n\n"
        "Just send me any message and I'll respond using AI!\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/clear - Clear conversation history\n"
        "/help - Show this message\n\n"
        "Developed by Abir 💙"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages and generate AI responses."""
    user_id = update.effective_user.id
    user_message = update.message.text
    user_name = update.effective_user.first_name
    
    # Initialize conversation history for new users
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    # Add user message to history
    conversation_history[user_id].append({
        "role": "user",
        "content": user_message
    })
    
    # Keep only last 10 messages to avoid token limits
    if len(conversation_history[user_id]) > 20:
        conversation_history[user_id] = conversation_history[user_id][-20:]
    
    try:
        # Send typing action
        await update.message.chat.send_action(action="typing")
        
        # Prepare messages for Groq
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history[user_id]
        
        # Get response from Groq
        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model="openai/gpt-oss-120b",
            temperature=0.7,
            max_tokens=1024,
        )
        
        ai_response = chat_completion.choices[0].message.content
        
        # Add AI response to history
        conversation_history[user_id].append({
            "role": "assistant",
            "content": ai_response
        })
        
        # Send response
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        await update.message.reply_text(
            "Sorry, I encountered an error processing your message. Please try again!"
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot."""
    # Get bot token from environment variable
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
        return
    
    # Create application
    application = Application.builder().token(bot_token).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_history))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Bot started successfully!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
