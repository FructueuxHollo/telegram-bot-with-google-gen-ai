import pytest
from bot.gemini_api import process_with_gemini

@pytest.fixture
def mock_gemini_client(monkeypatch):
    class MockClient:
        def models(self, *args, **kwargs):
            class MockResponse:
                @staticmethod
                def generate_content(*args, **kwargs):
                    class Result:
                        @property
                        def result(self):
                            return "Mock Gemini response"
                    return Result()
            return MockResponse()
    monkeypatch.setattr("bot.gemini_api.client", MockClient())

def test_process_with_gemini(mock_gemini_client):
    """Tests the Gemini API processing function."""
    response = process_with_gemini("Test input")
    assert response == "Mock Gemini response"
