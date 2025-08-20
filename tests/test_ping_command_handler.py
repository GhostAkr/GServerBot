import pytest
from unittest.mock import Mock, MagicMock
from telegram import Update, Message, Chat, User
from telegram.ext import ContextTypes

from src.commands.ping import PingCommandHandler


class TestPingCommandHandler:
    """Test cases for PingCommandHandler class."""
    
    @pytest.fixture
    def ping_handler(self):
        """Create a PingCommandHandler instance for testing."""
        return PingCommandHandler()
    
    @pytest.fixture
    def mock_update(self):
        """Create a mock Update object for testing."""
        update = Mock(spec=Update)
        update.message = Mock(spec=Message)
        update.message.reply_text = Mock()
        return update
    
    @pytest.fixture
    def mock_context(self):
        """Create a mock Context object for testing."""
        return Mock(spec=ContextTypes.DEFAULT_TYPE)
    
    def test_ping_handler_implements_icommand_handler(self, ping_handler):
        """Test that PingCommandHandler implements ICommandHandler interface."""
        from src.commands.icommand_handler import ICommandHandler
        assert isinstance(ping_handler, ICommandHandler)
    
    def test_ping_handler_name_returns_correct_command(self, ping_handler):
        """Test that the name method returns the correct command string."""
        assert ping_handler.name() == '/ping'
    
    @pytest.mark.asyncio
    async def test_ping_handler_handle_sends_correct_message(self, ping_handler, mock_update, mock_context):
        """Test that the handle method sends the correct reply message."""
        await ping_handler.handle(mock_update, mock_context)
        
        mock_update.message.reply_text.assert_called_once_with("I'm alive.")
    
    @pytest.mark.asyncio
    async def test_ping_handler_handle_calls_reply_text_on_message(self, ping_handler, mock_update, mock_context):
        """Test that handle method calls reply_text on the update message."""
        await ping_handler.handle(mock_update, mock_context)
        
        assert mock_update.message.reply_text.called
    
    @pytest.mark.asyncio
    async def test_ping_handler_handle_ignores_context_parameter(self, ping_handler, mock_update, mock_context):
        """Test that handle method works regardless of context content."""
        # Set some arbitrary values on context to ensure they're ignored
        mock_context.some_attribute = "test_value"
        mock_context.another_attribute = 123
        
        await ping_handler.handle(mock_update, mock_context)
        
        # Should still work and send the expected message
        mock_update.message.reply_text.assert_called_once_with("I'm alive.")
    
    @pytest.mark.asyncio
    async def test_ping_handler_handle_with_none_context(self, ping_handler, mock_update):
        """Test that handle method works with None context."""
        await ping_handler.handle(mock_update, None)
        
        mock_update.message.reply_text.assert_called_once_with("I'm alive.")
    
    @pytest.mark.asyncio
    async def test_ping_handler_handle_with_none_update_message(self, ping_handler, mock_context):
        """Test that handle method works when update.message is None."""
        update = Mock(spec=Update)
        update.message = None
        
        # This should raise an AttributeError since we can't call reply_text on None
        with pytest.raises(AttributeError):
            await ping_handler.handle(update, mock_context)
    
    @pytest.mark.asyncio
    async def test_ping_handler_handle_with_missing_reply_text_method(self, ping_handler, mock_context):
        """Test that handle method fails gracefully when reply_text method is missing."""
        update = Mock(spec=Update)
        update.message = Mock()
        # Remove the reply_text method to simulate missing method
        del update.message.reply_text
        
        with pytest.raises(AttributeError):
            await ping_handler.handle(update, mock_context)
    
    def test_ping_handler_instance_creation(self):
        """Test that PingCommandHandler can be instantiated."""
        handler = PingCommandHandler()
        assert handler is not None
        assert isinstance(handler, PingCommandHandler)
    
    def test_ping_handler_multiple_instances(self):
        """Test that multiple PingCommandHandler instances work independently."""
        handler1 = PingCommandHandler()
        handler2 = PingCommandHandler()
        
        assert handler1 is not handler2
        assert handler1.name() == handler2.name()
        assert handler1.name() == '/ping'
    
    @pytest.mark.asyncio
    async def test_ping_handler_handle_called_multiple_times(self, ping_handler, mock_update, mock_context):
        """Test that handle method can be called multiple times."""
        # First call
        await ping_handler.handle(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once_with("I'm alive.")
        
        # Reset mock for second call
        mock_update.message.reply_text.reset_mock()
        
        # Second call
        await ping_handler.handle(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once_with("I'm alive.")
