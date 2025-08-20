"""
Telegram bot implementation.
"""

from telegram.ext import ApplicationBuilder, CommandHandler
from icommand_handlers_manager import ICommandHandlersManager

class TelegramBot:
    """Main Telegram bot class."""
        
    def __init__(
        self,
        token: str,
        command_handlers_manager: ICommandHandlersManager
    ):
        """Initialize the bot with a token and command handlers manager."""
        self.token = token
        self.command_handlers_manager = command_handlers_manager

        applicationBuilder = ApplicationBuilder()
        applicationBuilder.token(token)

        self.application = applicationBuilder.build()
        
        # Register all command handlers
        self._register_command_handlers()
    
    def _register_command_handlers(self):
        """
        Register all command handlers with the bot application.
        
        This method goes through the list of registered handlers and registers
        each command in the bot.
        """
        handlers = self.get_registered_handlers()
        for handler in handlers:
            command_name = handler.name().lstrip('/')  # Remove leading slash for CommandHandler
            command_handler = CommandHandler(command_name, handler.handle)
            self.application.add_handler(command_handler)
    
    def run(self):
        """Start the bot."""
        try:
            self.application.run_polling()
        except KeyboardInterrupt:
            print("Stopping GServerBot...")
    
    def get_registered_handlers(self):
        """
        Get all registered command handlers from the command handlers manager.
        
        Returns:
            List[ICommandHandler]: A list of all registered handlers
        """
        return self.command_handlers_manager.get_registered_handlers()
