from typing import Optional
from commands.icommand_handler import ICommandHandler


class CommandHandlersRegistry:
    """
    Concrete implementation of command handlers registry.
    
    This class provides a dictionary-based storage for command handlers,
    allowing efficient addition, removal, and retrieval of handlers by command name.
    """
    
    def __init__(self):
        """Initialize an empty command handlers registry."""
        self._handlers: dict[str, ICommandHandler] = {}
    
    def add(self, handler: ICommandHandler) -> None:
        """
        Add a command handler to the registry.
        
        Args:
            handler (ICommandHandler): The command handler to add to the registry
            
        Raises:
            ValueError: If a handler with the same command name already exists
        """
        command_name = handler.name()
        if command_name in self._handlers:
            raise ValueError(f"Handler for command '{command_name}' already exists")
        
        self._handlers[command_name] = handler
    
    def remove(self, command: str) -> None:
        """
        Remove a command handler from the registry by command name.
        
        Args:
            command (str): The command name to remove (e.g., '/start', '/help')
            
        Raises:
            KeyError: If no handler exists for the specified command
        """
        if command not in self._handlers:
            raise KeyError(f"No handler found for command '{command}'")
        
        del self._handlers[command]
    
    def get(self, command: str) -> Optional[ICommandHandler]:
        """
        Get a command handler from the registry by command name.
        
        Args:
            command (str): The command name to retrieve (e.g., '/start', '/help')
            
        Returns:
            Optional[ICommandHandler]: The command handler if found, None otherwise
        """
        return self._handlers.get(command)
    
    def get_all_handlers(self) -> dict[str, ICommandHandler]:
        """
        Get all registered command handlers.
        
        Returns:
            dict[str, ICommandHandler]: A copy of all registered handlers
        """
        return self._handlers.copy()
    
    def has_handler(self, command: str) -> bool:
        """
        Check if a handler exists for the specified command.
        
        Args:
            command (str): The command name to check
            
        Returns:
            bool: True if a handler exists, False otherwise
        """
        return command in self._handlers
    
    def count(self) -> int:
        """
        Get the total number of registered handlers.
        
        Returns:
            int: The number of registered handlers
        """
        return len(self._handlers)
