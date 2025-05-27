import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Load test environment variables if in test environment
if os.getenv("TESTING") == "true":
    test_env_path = Path(__file__).parent.parent / ".env.test"
    if test_env_path.exists():
        load_dotenv(test_env_path)

# Get environment variables with defaults for testing
AI_BASE_URL = os.getenv("AI_BASE_URL", "http://mock-ai-server.test")
