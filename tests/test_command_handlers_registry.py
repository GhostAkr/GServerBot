import pytest
from unittest.mock import Mock
from src.command_handlers_registry import CommandHandlersRegistry
from src.commands.icommand_handler import ICommandHandler


class MockCommandHandler(ICommandHandler):
    """Mock command handler for testing purposes."""
    
    def __init__(self, command_name: str):
        self._command_name = command_name
    
    def handle(self, update, context):
        pass
    
    def name(self) -> str:
        return self._command_name


class TestCommandHandlersRegistry:
    """Test cases for CommandHandlersRegistry class."""
    
    def test_init(self):
        """Test registry initialization."""
        registry = CommandHandlersRegistry()
        assert registry.count() == 0
        assert not registry.has_handler('/test')
    
    def test_add_handler(self):
        """Test adding a command handler."""
        registry = CommandHandlersRegistry()
        handler = MockCommandHandler('/test')
        
        registry.add(handler)
        
        assert registry.count() == 1
        assert registry.has_handler('/test')
        assert registry.get('/test') == handler
    
    def test_add_duplicate_handler(self):
        """Test adding a handler with duplicate command name."""
        registry = CommandHandlersRegistry()
        handler1 = MockCommandHandler('/test')
        handler2 = MockCommandHandler('/test')
        
        registry.add(handler1)
        
        with pytest.raises(ValueError, match="Handler for command '/test' already exists"):
            registry.add(handler2)
    
    def test_remove_handler(self):
        """Test removing a command handler."""
        registry = CommandHandlersRegistry()
        handler = MockCommandHandler('/test')
        
        registry.add(handler)
        assert registry.count() == 1
        
        registry.remove('/test')
        
        assert registry.count() == 0
        assert not registry.has_handler('/test')
        assert registry.get('/test') is None
    
    def test_remove_nonexistent_handler(self):
        """Test removing a handler that doesn't exist."""
        registry = CommandHandlersRegistry()
        
        with pytest.raises(KeyError, match="No handler found for command '/test'"):
            registry.remove('/test')
    
    def test_get_handler(self):
        """Test getting a command handler."""
        registry = CommandHandlersRegistry()
        handler = MockCommandHandler('/test')
        
        registry.add(handler)
        
        retrieved_handler = registry.get('/test')
        assert retrieved_handler == handler
    
    def test_get_nonexistent_handler(self):
        """Test getting a handler that doesn't exist."""
        registry = CommandHandlersRegistry()
        
        handler = registry.get('/test')
        assert handler is None
    
    def test_get_all_handlers(self):
        """Test getting all registered handlers."""
        registry = CommandHandlersRegistry()
        handler1 = MockCommandHandler('/test1')
        handler2 = MockCommandHandler('/test2')
        
        registry.add(handler1)
        registry.add(handler2)
        
        all_handlers = registry.get_all_handlers()
        
        assert len(all_handlers) == 2
        assert handler1 in all_handlers
        assert handler2 in all_handlers
        
        # Test that returned list is a copy, not the original
        all_handlers.append(MockCommandHandler('/test3'))
        assert registry.count() == 2
    
    def test_has_handler(self):
        """Test checking if a handler exists."""
        registry = CommandHandlersRegistry()
        handler = MockCommandHandler('/test')
        
        assert not registry.has_handler('/test')
        
        registry.add(handler)
        
        assert registry.has_handler('/test')
    
    def test_count(self):
        """Test counting registered handlers."""
        registry = CommandHandlersRegistry()
        assert registry.count() == 0
        
        handler1 = MockCommandHandler('/test1')
        registry.add(handler1)
        assert registry.count() == 1
        
        handler2 = MockCommandHandler('/test2')
        registry.add(handler2)
        assert registry.count() == 2
        
        registry.remove('/test1')
        assert registry.count() == 1
