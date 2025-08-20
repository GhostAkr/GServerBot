from .icommand_handler import ICommandHandler
from telegram import Update
from telegram.ext import ContextTypes


class PingCommandHandler(ICommandHandler):
    """Command handler for the /ping command."""
    
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle the /ping command by sending "I'm alive." message.

        Args:
            update (telegram.Update): The Telegram update object containing the command.
            context (telegram.ext.ContextTypes.DEFAULT_TYPE): The Telegram bot context object.
        """
        await update.message.reply_text("I'm alive.")
    
    def name(self) -> str:
        """Get the command name for this handler."""
        return '/ping'
