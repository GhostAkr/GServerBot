from abc import ABC, abstractmethod


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
