from dotenv import load_dotenv, find_dotenv
import os
import sys

load_dotenv(find_dotenv())

_env = os.environ


AI_BASE_URL = _env["AI_BASE_URL"]
