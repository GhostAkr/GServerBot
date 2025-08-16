from icommand_handlers_manager import ICommandHandlersManager
from icommand_handlers_registry import ICommandHandlersRegistry
from commands.ping import PingCommandHandler


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
        
        This method adds the PingCommandHandler to the handlers registry.
        """
        ping_handler = PingCommandHandler()
        self._registry.add(ping_handler)
    
    def register(self) -> None:
        """
        Register all handlers in the bot.
        
        This method currently does nothing as specified in the requirements.
        """
        pass
