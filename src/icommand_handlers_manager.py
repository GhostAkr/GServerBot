from abc import ABC, abstractmethod
from typing import List
from commands.icommand_handler import ICommandHandler


class ICommandHandlersManager(ABC):
    """
    Abstract interface for command handlers manager.
    
    This interface defines the contract for managing command handlers in the bot.
    """
    
    @abstractmethod
    def populate_bot_handlers(self) -> None:
        """
        Populate all command handlers in CommandHandlersRegistry.
        """
        pass
    
    @abstractmethod
    def get_registered_handlers(self) -> List[ICommandHandler]:
        """
        Get all registered command handlers from the registry.
        
        Returns:
            List[ICommandHandler]: A list of all registered handlers
        """
        pass
