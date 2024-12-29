from bot.utils import format_response

def test_format_response():
    """Tests the response formatting utility."""
    input_text = "Hello, world!"
    formatted_text = format_response(input_text)
    assert formatted_text == "Bot Reply:\nHello, world!"
