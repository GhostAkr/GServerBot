import pytest
from unittest.mock import Mock, MagicMock
from src.bot import TelegramBot
from src.command_handlers_manager import CommandHandlersManager
from src.command_handlers_registry import CommandHandlersRegistry
from commands.ping import PingCommandHandler


class TestTelegramBot:
    """Test cases for TelegramBot class."""
    
    @pytest.fixture
    def mock_command_handlers_manager(self):
        """Create a mock command handlers manager for testing."""
        return Mock()
    
    @pytest.fixture
    def concrete_command_handlers_manager(self):
        """Create a concrete command handlers manager for integration testing."""
        registry = CommandHandlersRegistry()
        return CommandHandlersManager(registry)
    
    @pytest.fixture
    def bot_with_mock_manager(self, mock_command_handlers_manager):
        """Create a TelegramBot with a mock command handlers manager."""
        return TelegramBot("test_token", mock_command_handlers_manager)
    
    @pytest.fixture
    def bot_with_concrete_manager(self, concrete_command_handlers_manager):
        """Create a TelegramBot with a concrete command handlers manager."""
        return TelegramBot("test_token", concrete_command_handlers_manager)
    
    def test_bot_implements_get_registered_handlers(self, bot_with_mock_manager):
        """Test that TelegramBot has the get_registered_handlers method."""
        assert hasattr(bot_with_mock_manager, 'get_registered_handlers')
        assert callable(bot_with_mock_manager.get_registered_handlers)
    
    def test_get_registered_handlers_calls_manager_method(self, bot_with_mock_manager, mock_command_handlers_manager):
        """Test that get_registered_handlers calls the manager's get_registered_handlers method."""
        # Mock the manager's get_registered_handlers method to return a list
        mock_handlers = [Mock(), Mock()]
        mock_command_handlers_manager.get_registered_handlers.return_value = mock_handlers
        
        result = bot_with_mock_manager.get_registered_handlers()
        
        # Verify the result
        assert result == mock_handlers
        
        # Verify the manager method was called
        mock_command_handlers_manager.get_registered_handlers.assert_called_once()
    
    def test_get_registered_handlers_returns_empty_list_when_no_handlers(self, bot_with_concrete_manager):
        """Test that get_registered_handlers returns empty list when no handlers are registered."""
        handlers = bot_with_concrete_manager.get_registered_handlers()
        assert len(handlers) == 0
    
    def test_get_registered_handlers_returns_handlers_after_population(self, bot_with_concrete_manager):
        """Test that get_registered_handlers returns handlers after they are populated."""
        # Initially no handlers
        handlers = bot_with_concrete_manager.get_registered_handlers()
        assert len(handlers) == 0
        
        # Populate handlers using the manager
        bot_with_concrete_manager.command_handlers_manager.populate_bot_handlers()
        
        # Get handlers again
        handlers = bot_with_concrete_manager.get_registered_handlers()
        assert len(handlers) == 1
        
        # Verify the handler is correct
        ping_handler = handlers[0]
        assert isinstance(ping_handler, PingCommandHandler)
        assert ping_handler.name() == '/ping'
    
    def test_get_registered_handlers_with_multiple_handlers(self, bot_with_concrete_manager):
        """Test that get_registered_handlers works with multiple handlers."""
        # Add multiple handlers to the registry
        from commands.icommand_handler import ICommandHandler
        
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
        
        # Add handlers directly to the registry
        registry = bot_with_concrete_manager.command_handlers_manager._registry
        registry.add(MockHandler1())
        registry.add(MockHandler2())
        
        # Populate with ping handler
        bot_with_concrete_manager.command_handlers_manager.populate_bot_handlers()
        
        # Get all handlers
        handlers = bot_with_concrete_manager.get_registered_handlers()
        assert len(handlers) == 3
        
        # Verify all handlers are present
        handler_names = [handler.name() for handler in handlers]
        assert '/mock1' in handler_names
        assert '/mock2' in handler_names
        assert '/ping' in handler_names
    
    def test_get_registered_handlers_returns_correct_handler_types(self, bot_with_concrete_manager):
        """Test that get_registered_handlers returns handlers of the correct type."""
        # Populate handlers
        bot_with_concrete_manager.command_handlers_manager.populate_bot_handlers()
        
        # Get handlers
        handlers = bot_with_concrete_manager.get_registered_handlers()
        
        # Verify all handlers implement ICommandHandler
        from commands.icommand_handler import ICommandHandler
        for handler in handlers:
            assert isinstance(handler, ICommandHandler)
    
    def test_get_registered_handlers_returns_fresh_list_each_time(self, bot_with_concrete_manager):
        """Test that get_registered_handlers returns a fresh list each time it's called."""
        # Populate handlers
        bot_with_concrete_manager.command_handlers_manager.populate_bot_handlers()
        
        # Get handlers twice
        handlers1 = bot_with_concrete_manager.get_registered_handlers()
        handlers2 = bot_with_concrete_manager.get_registered_handlers()
        
        # Verify they are different list instances but contain the same handlers
        assert handlers1 is not handlers2
        assert handlers1 == handlers2
        assert len(handlers1) == len(handlers2) == 1
    
    def test_bot_initialization_with_manager(self, mock_command_handlers_manager):
        """Test that TelegramBot initializes correctly with a command handlers manager."""
        bot = TelegramBot("test_token", mock_command_handlers_manager)
        
        assert bot.token == "test_token"
        assert bot.command_handlers_manager == mock_command_handlers_manager
        assert hasattr(bot, 'application')
    
    def test_bot_has_required_attributes(self, bot_with_mock_manager):
        """Test that TelegramBot has all required attributes."""
        bot = bot_with_mock_manager
        
        assert hasattr(bot, 'token')
        assert hasattr(bot, 'command_handlers_manager')
        assert hasattr(bot, 'application')
        assert hasattr(bot, 'run')
        assert hasattr(bot, 'get_registered_handlers')
