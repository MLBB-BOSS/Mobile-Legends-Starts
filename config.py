# File: config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Other configuration constants
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
