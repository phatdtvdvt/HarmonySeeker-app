import sys
import os
import base64
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import pytest
import asyncio

# Ensure the parent directory is in the import path if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.fixture
def ai_response_data():
    # Mock base64 encoded audio data
    return {
        "vocals": base64.b64encode(b"mock_vocals_audio_data").decode(),
        "instrumental": base64.b64encode(b"mock_instrumental_audio_data").decode(),
    }


@pytest.fixture
def mock_async_post(ai_response_data):
    async def _mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 200

            def json(self):
                return ai_response_data

            @property
            def text(self):
                return "Success"

        return MockResponse()

    return _mock_post


@pytest.mark.asyncio
async def test_separate_voice_endpoint(mock_async_post):
    # Create a mock file
    test_file_content = b"test audio content"

    with patch("httpx.AsyncClient.post", new=mock_async_post):
        # Simulate file upload
        response = client.post(
            "/api/separate-voice",
            files={"file": ("test.mp3", test_file_content, "audio/mpeg")},
        )

        assert response.status_code == 200
        response_data = response.json()

        # Check if both audio files are in the response as base64 strings
        assert "vocals" in response_data
        assert "instrumental" in response_data
        assert isinstance(response_data["vocals"], str)
        assert isinstance(response_data["instrumental"], str)

        # Verify the content can be decoded from base64
        assert base64.b64decode(response_data["vocals"])
        assert base64.b64decode(response_data["instrumental"])


@pytest.mark.asyncio
async def test_separate_voice_ai_server_error():
    async def mock_error_response(*args, **kwargs):
        class MockResponse:
            status_code = 500
            text = "AI Server Error"

            def json(self):
                return {"error": "AI Server Error"}

        return MockResponse()

    test_file_content = b"test audio content"

    with patch("httpx.AsyncClient.post", new=mock_error_response):
        response = client.post(
            "/api/separate-voice",
            files={"file": ("test.mp3", test_file_content, "audio/mpeg")},
        )

        assert response.status_code == 500
        assert response.json()["error"] == "AI server error"


@pytest.mark.asyncio
async def test_separate_voice_invalid_file():
    # Test with empty file
    response = client.post(
        "/api/separate-voice", files={"file": ("test.mp3", b"", "audio/mpeg")}
    )

    assert response.status_code == 500  # Should handle empty file error


@pytest.mark.asyncio
async def test_separate_voice_missing_file():
    # Test without providing any file
    response = client.post("/api/separate-voice")

    assert response.status_code == 422  # FastAPI validation error
