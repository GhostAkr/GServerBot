"""
Telegram bot implementation.
"""

from telegram.ext import ApplicationBuilder

class TelegramBot:
    """Main Telegram bot class."""
    
    def __init__(self, token: str):
        """Initialize the bot with a token."""
        self.token = token

        applicationBuilder = ApplicationBuilder()
        applicationBuilder.token(token)

        self.application = applicationBuilder.build()
    
    def run(self):
        """Start the bot."""
        try:
            self.application.run_polling()
        except KeyboardInterrupt:
            print("Stopping GServerBot...")
