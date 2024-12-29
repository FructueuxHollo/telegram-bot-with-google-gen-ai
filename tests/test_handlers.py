import pytest
from telegram import Update, Message
from telegram.ext import CallbackContext
from bot.handlers import start, handle_message

@pytest.fixture
def mock_update():
    """Creates a mock Update object."""
    return Update(
        update_id=1,
        message=Message(
            message_id=1,
            date=None,
            chat=None,
            text="Test message",
            bot=None,
            reply_to_message=None,
        )
    )

@pytest.fixture
def mock_context():
    """Creates a mock CallbackContext object."""
    return CallbackContext(dispatcher=None)

def test_start(mock_update, mock_context):
    """Tests the /start handler."""
    start(mock_update, mock_context)
    # Assert that the bot sends the correct welcome message
    assert mock_update.message.reply_text.call_count == 1

def test_handle_message(mock_update, mock_context, monkeypatch):
    """Tests the message handler."""
    def mock_process_with_gemini(input_text):
        return "Mock response from Gemini"

    monkeypatch.setattr("bot.gemini_api.process_with_gemini", mock_process_with_gemini)

    handle_message(mock_update, mock_context)
    assert mock_update.message.reply_text.call_count == 1
    assert "Mock response from Gemini" in str(mock_update.message.reply_text.call_args)
