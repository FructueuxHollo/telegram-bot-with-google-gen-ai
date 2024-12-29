from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from gemini_api import process_with_gemini

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    welcome_message = (
        "👋 Hello! I'm a bot powered by Google's Gemini AI.\n\n"
        "You can start chatting with me by sending any message!"
    )
    await update.message.reply_text(welcome_message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages using Gemini AI"""
    try:
        user_input = update.message.text
        
        # Send typing action
        await context.bot.send_chat_action(
            chat_id=update.message.chat_id,
            action=ChatAction.TYPING
        )
        
        # Get response from Gemini
        response_text = await process_with_gemini(user_input)
        
        if not response_text:
            raise ValueError("Empty response from Gemini API")
        
        # Split long messages if needed (Telegram has a 4096 character limit)
        if len(response_text) > 4000:
            chunks = [response_text[i:i+4000] for i in range(0, len(response_text), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(response_text)
                
    except Exception as e:
        error_message = (
            "I apologize, but I encountered an error while processing your message. "
            "Please try again later."
        )
        await update.message.reply_text(error_message)
        # Log the error for debugging
        print(f"Error in handle_message: {str(e)}")

def setup_handlers(application):
    """Set up all handlers for the application"""
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    application.add_error_handler(lambda update, context: print(f"Error: {context.error}"))