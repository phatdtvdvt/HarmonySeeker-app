import sys
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import pytest
import asyncio

# Ensure the parent directory is in the import path if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import (
    app,
)  # Make sure main.py contains `app = FastAPI()` and includes the router

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.fixture
def ai_response_data():
    return {
        "main_chord": "C",
        "key": "C",
        "chord_sequence": ["C", "C", "G", "G", "Am", "Am", "F", "F"],
    }


@pytest.fixture
def mock_async_post(ai_response_data):
    async def _mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 200

            def json(self):
                return ai_response_data

        return MockResponse()

    return _mock_post
