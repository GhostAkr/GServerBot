"""
Main entry point for the Telegram bot.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from bot import TelegramBot

# Load environment variables from .env file
load_dotenv()


def main():
    """Main function to run the Telegram bot."""
    # Get bot token from environment variable
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is not set.")
        return
    
    try:
        bot = TelegramBot(bot_token)
        bot.run()
    except KeyboardInterrupt:
        print("\nThe bot stopped by the user.")
    except Exception as e:
        print(f"Error running the bot: {e}")


if __name__ == "__main__":
    main()
