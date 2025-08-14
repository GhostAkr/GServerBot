from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes


class ICommandHandler(ABC):
    """
    Abstract interface for Telegram bot command handlers.
    
    This interface defines the contract that all command handlers must implement.
    """
    
    @abstractmethod
    def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handle the command execution.
        
        Args:
            update: The Telegram update object containing the command
            context: The Telegram bot context object
        """
        pass
    
    @abstractmethod
    def name(self) -> str:
        """
        Get the command name that this handler responds to.
        
        Returns:
            The command name as a string (e.g., '/start', '/help')
        """
        pass 
