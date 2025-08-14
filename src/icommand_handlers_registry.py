from abc import ABC, abstractmethod
from .commands.icommand_handler import ICommandHandler


class ICommandHandlersRegistry(ABC):
    """
    Abstract interface for command handlers registry.
    
    This interface defines the contract for managing command handlers in the bot.
    """
    
    @abstractmethod
    def add(self, handler: ICommandHandler) -> None:
        """
        Add a command handler to the registry.
        
        Args:
            handler (ICommandHandler): The command handler to add to the registry
        """
        pass
    
    @abstractmethod
    def remove(self, command: str) -> None:
        """
        Remove a command handler from the registry by command name.
        
        Args:
            command (str): The command name to remove (e.g., '/start', '/help')
        """
        pass
