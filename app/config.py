# config.py
# Purpose: Load environment variables (like API keys) in one central place
# so the rest of the app never touches .env directly.

import os
from dotenv import load_dotenv

# Load variables from .env file into the environment
load_dotenv()

# Read the OpenAI API key; raise an error early if it's missing
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing. Check your .env file.")