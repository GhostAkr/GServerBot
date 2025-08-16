"""
Telegram bot implementation.
"""

from telegram.ext import ApplicationBuilder
from icommand_handlers_registry import ICommandHandlersRegistry

class TelegramBot:
    """Main Telegram bot class."""
    
    def __init__(self, token: str, command_handlers_registry: ICommandHandlersRegistry):
        """Initialize the bot with a token and command handlers registry."""
        self.token = token
        self.command_handlers_registry = command_handlers_registry

        applicationBuilder = ApplicationBuilder()
        applicationBuilder.token(token)

        self.application = applicationBuilder.build()
    
    def run(self):
        """Start the bot."""
        try:
            self.application.run_polling()
        except KeyboardInterrupt:
            print("Stopping GServerBot...")
