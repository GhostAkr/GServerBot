import pytest
from unittest.mock import Mock, MagicMock
from src.command_handlers_manager import CommandHandlersManager
from src.command_handlers_registry import CommandHandlersRegistry
from src.commands.ping import PingCommandHandler


class TestCommandHandlersManager:
    """Test cases for CommandHandlersManager class."""
    
    @pytest.fixture
    def mock_registry(self):
        """Create a mock registry for testing."""
        return Mock(spec=CommandHandlersRegistry)
    
    @pytest.fixture
    def concrete_registry(self):
        """Create a concrete registry instance for integration testing."""
        return CommandHandlersRegistry()
    
    @pytest.fixture
    def manager_with_mock(self, mock_registry):
        """Create a CommandHandlersManager with a mock registry."""
        return CommandHandlersManager(mock_registry)
    
    @pytest.fixture
    def manager_with_concrete(self, concrete_registry):
        """Create a CommandHandlersManager with a concrete registry."""
        return CommandHandlersManager(concrete_registry)
    
    def test_manager_implements_icommand_handlers_manager(self, manager_with_mock):
        """Test that CommandHandlersManager implements ICommandHandlersManager interface."""
        from icommand_handlers_manager import ICommandHandlersManager
        assert isinstance(manager_with_mock, ICommandHandlersManager)
    
    def test_manager_initialization(self, mock_registry):
        """Test that CommandHandlersManager initializes correctly with a registry."""
        manager = CommandHandlersManager(mock_registry)
        assert manager._registry == mock_registry
    
    def test_manager_initialization_with_concrete_registry(self, concrete_registry):
        """Test that CommandHandlersManager initializes correctly with a concrete registry."""
        manager = CommandHandlersManager(concrete_registry)
        assert manager._registry == concrete_registry
    
    def test_populate_bot_handlers_calls_registry_add(self, manager_with_mock, mock_registry):
        """Test that populate_bot_handlers calls the registry's add method."""
        manager_with_mock.populate_bot_handlers()
        
        # Verify that add was called once
        mock_registry.add.assert_called_once()
        
        # Verify that the argument passed to add is a PingCommandHandler
        call_args = mock_registry.add.call_args
        assert len(call_args[0]) == 1
        # Check the actual type from the import path used in the manager
        from commands.ping import PingCommandHandler as ActualPingHandler
        assert isinstance(call_args[0][0], ActualPingHandler)
    
    def test_populate_bot_handlers_creates_ping_handler(self, manager_with_mock, mock_registry):
        """Test that populate_bot_handlers creates a PingCommandHandler instance."""
        manager_with_mock.populate_bot_handlers()
        
        # Get the handler that was passed to add
        call_args = mock_registry.add.call_args
        ping_handler = call_args[0][0]
        
        # Verify it's a PingCommandHandler with correct command name
        from commands.ping import PingCommandHandler as ActualPingHandler
        assert isinstance(ping_handler, ActualPingHandler)
        assert ping_handler.name() == '/ping'
    
    def test_populate_bot_handlers_integration_with_concrete_registry(self, manager_with_concrete, concrete_registry):
        """Test that populate_bot_handlers works with a concrete registry."""
        # Initially no handlers
        assert concrete_registry.count() == 0
        assert not concrete_registry.has_handler('/ping')
        
        # Populate handlers
        manager_with_concrete.populate_bot_handlers()
        
        # Verify handler was added
        assert concrete_registry.count() == 1
        assert concrete_registry.has_handler('/ping')
        
        # Verify the handler is retrievable
        ping_handler = concrete_registry.get('/ping')
        from commands.ping import PingCommandHandler as ActualPingHandler
        assert isinstance(ping_handler, ActualPingHandler)
        assert ping_handler.name() == '/ping'
    
    def test_populate_bot_handlers_multiple_calls(self, manager_with_mock, mock_registry):
        """Test that populate_bot_handlers can be called multiple times."""
        # First call
        manager_with_mock.populate_bot_handlers()
        assert mock_registry.add.call_count == 1
        
        # Reset mock for second call
        mock_registry.add.reset_mock()
        
        # Second call
        manager_with_mock.populate_bot_handlers()
        assert mock_registry.add.call_count == 1
        
        # Verify both calls created PingCommandHandler instances
        call_args = mock_registry.add.call_args
        ping_handler = call_args[0][0]
        from commands.ping import PingCommandHandler as ActualPingHandler
        assert isinstance(ping_handler, ActualPingHandler)
    
    def test_populate_bot_handlers_registry_error_handling(self, manager_with_mock, mock_registry):
        """Test that populate_bot_handlers handles registry errors gracefully."""
        # Make the registry.add method raise an exception
        mock_registry.add.side_effect = ValueError("Test error")
        
        # This should propagate the error
        with pytest.raises(ValueError, match="Test error"):
            manager_with_mock.populate_bot_handlers()
    
    
    def test_manager_with_none_registry_works(self):
        """Test that CommandHandlersManager can be initialized with None registry (current behavior)."""
        # Note: This test reflects the current implementation behavior
        # In a production system, you might want to add type checking
        manager = CommandHandlersManager(None)
        assert manager._registry is None
    
    def test_manager_with_invalid_registry_type_works(self):
        """Test that CommandHandlersManager can be initialized with invalid registry type (current behavior)."""
        # Note: This test reflects the current implementation behavior
        # In a production system, you might want to add type checking
        invalid_registry = "not a registry"
        manager = CommandHandlersManager(invalid_registry)
        assert manager._registry == invalid_registry
    
    def test_manager_attributes_are_protected(self, manager_with_mock):
        """Test that manager attributes are properly protected (start with underscore)."""
        # The _registry attribute should be protected
        assert hasattr(manager_with_mock, '_registry')
        
        # Direct access should still work for testing purposes
        assert manager_with_mock._registry is not None
    
    def test_populate_bot_handlers_creates_fresh_handler_each_time(self, manager_with_mock, mock_registry):
        """Test that populate_bot_handlers creates a fresh PingCommandHandler each time."""
        # First call
        manager_with_mock.populate_bot_handlers()
        first_handler = mock_registry.add.call_args[0][0]
        
        # Reset mock
        mock_registry.add.reset_mock()
        
        # Second call
        manager_with_mock.populate_bot_handlers()
        second_handler = mock_registry.add.call_args[0][0]
        
        # Verify they are different instances
        assert first_handler is not second_handler
        assert first_handler.name() == second_handler.name() == '/ping'
    
    def test_manager_works_with_empty_registry(self, concrete_registry):
        """Test that manager works correctly with an initially empty registry."""
        manager = CommandHandlersManager(concrete_registry)
        
        # Verify registry starts empty
        assert concrete_registry.count() == 0
        
        # Populate handlers
        manager.populate_bot_handlers()
        
        # Verify handler was added
        assert concrete_registry.count() == 1
        assert concrete_registry.has_handler('/ping')
    
    def test_manager_works_with_registry_containing_other_handlers(self, concrete_registry):
        """Test that manager works correctly when registry already contains other handlers."""
        # Add a different handler first
        from src.commands.icommand_handler import ICommandHandler
        
        class MockHandler(ICommandHandler):
            def handle(self, update, context):
                pass
            
            def name(self) -> str:
                return '/mock'
        
        concrete_registry.add(MockHandler())
        assert concrete_registry.count() == 1
        
        # Now create manager and populate
        manager = CommandHandlersManager(concrete_registry)
        manager.populate_bot_handlers()
        
        # Verify both handlers exist
        assert concrete_registry.count() == 2
        assert concrete_registry.has_handler('/mock')
        assert concrete_registry.has_handler('/ping')
    
    def test_get_registered_handlers_returns_list(self, manager_with_mock, mock_registry):
        """Test that get_registered_handlers returns a list of handlers."""
        # Mock the registry's get_all_handlers method to return a list
        mock_handlers = [Mock(), Mock()]
        mock_registry.get_all_handlers.return_value = mock_handlers
        
        result = manager_with_mock.get_registered_handlers()
        
        assert result == mock_handlers
        mock_registry.get_all_handlers.assert_called_once()
    
    def test_get_registered_handlers_integration_with_concrete_registry(self, manager_with_concrete, concrete_registry):
        """Test that get_registered_handlers works with a concrete registry."""
        # Initially no handlers
        handlers = manager_with_concrete.get_registered_handlers()
        assert len(handlers) == 0
        
        # Populate handlers
        manager_with_concrete.populate_bot_handlers()
        
        # Get handlers again
        handlers = manager_with_concrete.get_registered_handlers()
        assert len(handlers) == 1
        
        # Verify the handler is correct
        ping_handler = handlers[0]
        from commands.ping import PingCommandHandler as ActualPingHandler
        assert isinstance(ping_handler, ActualPingHandler)
        assert ping_handler.name() == '/ping'
    
    def test_get_registered_handlers_delegates_to_registry(self, manager_with_mock, mock_registry):
        """Test that get_registered_handlers properly delegates to the registry."""
        # Mock the registry's get_all_handlers method
        mock_registry.get_all_handlers.return_value = []
        
        # Call the manager method
        manager_with_mock.get_registered_handlers()
        
        # Verify the registry method was called
        mock_registry.get_all_handlers.assert_called_once()
    
    def test_get_registered_handlers_with_multiple_handlers(self, manager_with_concrete, concrete_registry):
        """Test that get_registered_handlers works with multiple handlers."""
        # Add multiple handlers
        from src.commands.icommand_handler import ICommandHandler
        
        class MockHandler1(ICommandHandler):
            def handle(self, update, context):
                pass
            
            def name(self) -> str:
                return '/mock1'
        
        class MockHandler2(ICommandHandler):
            def handle(self, update, context):
                pass
            
            def name(self) -> str:
                return '/mock2'
        
        concrete_registry.add(MockHandler1())
        concrete_registry.add(MockHandler2())
        
        # Populate with ping handler
        manager_with_concrete.populate_bot_handlers()
        
        # Get all handlers
        handlers = manager_with_concrete.get_registered_handlers()
        assert len(handlers) == 3
        
        # Verify all handlers are present
        handler_names = [handler.name() for handler in handlers]
        assert '/mock1' in handler_names
        assert '/mock2' in handler_names
        assert '/ping' in handler_names
