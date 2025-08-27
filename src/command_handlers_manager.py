from icommand_handlers_manager import ICommandHandlersManager
from icommand_handlers_registry import ICommandHandlersRegistry
from commands.ping import PingCommandHandler
from typing import List
from commands.icommand_handler import ICommandHandler


class CommandHandlersManager(ICommandHandlersManager):
    """
    Concrete implementation of command handlers manager.
    
    This class manages the population and registration of command handlers
    in the bot system.
    """
    
    def __init__(self, registry: ICommandHandlersRegistry):
        """
        Initialize the command handlers manager with a registry instance.
        
        Args:
            registry (ICommandHandlersRegistry): The command handlers registry to use
        """
        self._registry = registry
    
    def populate_bot_handlers(self) -> None:
        """
        Populate all command handlers in CommandHandlersRegistry.
        
        This method adds concrete command handlers to the handlers registry.
        """
        self._registry.add(PingCommandHandler())
    
    def get_registered_handlers(self) -> List[ICommandHandler]:
        """
        Get all registered command handlers from the registry.
        
        Returns:
            List[ICommandHandler]: A list of all registered handlers
        """
        return self._registry.get_all_handlers()
