import asyncio
import sys
from telegram import Update
from telegram.ext import Application
from handlers import setup_handlers
from config import TELEGRAM_BOT_TOKEN

async def main():
    """Main function to run the bot"""
    app = None
    try:
        print("Initializing the bot...")
        # Build and initialize the application
        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        await app.initialize()
        print("Application built and initialized successfully.")
        
        # Setting up handlers
        try:
            print("Setting up handlers...")
            setup_handlers(app)
            print("Handlers set up successfully.")
        except Exception as e:
            print(f"Error during handler setup: {e}")
            raise
            
        # Start polling
        print("Starting bot polling...")
        await app.start()
        await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        
        # Keep the bot running until interrupted
        print("Bot is running. Press Ctrl+C to stop.")
        stopping = asyncio.Event()
        await stopping.wait()
        
    except Exception as e:
        print(f"Unexpected error in main function: {e}")
        raise
    finally:
        if app:
            print("Shutting down the bot...")
            try:
                if hasattr(app.updater, 'running') and app.updater.running:
                    await app.updater.stop()
                await app.stop()
                await app.shutdown()
                print("Bot shut down successfully.")
            except Exception as e:
                print(f"Error during shutdown: {e}")

def run_bot():
    """Wrapper function to run the bot with proper error handling"""
    if sys.platform.startswith('win'):
        print("Detected Windows platform. Setting Windows event loop policy...")
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    try:
        print("Starting the application...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped gracefully.")
    except Exception as e:
        print(f"Fatal error in the main execution: {e}")

if __name__ == "__main__":
    run_bot()