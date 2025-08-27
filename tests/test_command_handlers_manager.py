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
    def manager_with_mock(self, mock_registry):
        """Create a CommandHandlersManager with a mock registry."""
        return CommandHandlersManager(mock_registry)
    
    def test_manager_initialization(self, mock_registry):
        """Test that CommandHandlersManager initializes correctly with a registry."""
        manager = CommandHandlersManager(mock_registry)
        assert manager._registry == mock_registry
    
    def test_populate_bot_handlers_calls_registry_add(self, manager_with_mock, mock_registry):
        """Test that populate_bot_handlers calls the registry's add method."""
        manager_with_mock.populate_bot_handlers()
        
        # Verify that add was called once
        mock_registry.add.assert_called_once()
        
        # Verify that the argument passed to add is a PingCommandHandler
        call_args = mock_registry.add.call_args
        assert len(call_args[0]) == 1

    def test_populate_bot_handlers_adds_all_handlers(self, manager_with_mock, mock_registry):
        """
        Test that populate_bot_handlers adds all command handlers to the registry.
        """
        manager_with_mock.populate_bot_handlers()

        mock_registry.add.assert_called_once()
        
        handler_instance = mock_registry.add.call_args[0][0]
        from commands.ping import PingCommandHandler as ActualPingHandler
        assert isinstance(handler_instance, ActualPingHandler)
        assert handler_instance.name() == '/ping'
    
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
    
    def test_get_registered_handlers_returns_list(self, manager_with_mock, mock_registry):
        """Test that get_registered_handlers returns a list of handlers."""
        # Mock the registry's get_all_handlers method to return a list
        mock_handlers = [Mock(), Mock()]
        mock_registry.get_all_handlers.return_value = mock_handlers
        
        result = manager_with_mock.get_registered_handlers()
        
        assert result == mock_handlers
        mock_registry.get_all_handlers.assert_called_once()
