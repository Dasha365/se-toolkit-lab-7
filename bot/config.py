"""Configuration - loads environment variables from .env.bot.secret.

Usage:
    from config import settings
    
    # Access settings
    bot_token = settings.BOT_TOKEN
    lms_url = settings.LMS_API_BASE_URL
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env.bot.secret from the bot directory
BOT_DIR = Path(__file__).parent
ENV_FILE = BOT_DIR / ".env.bot.secret"

# Load environment variables (only if file exists)
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)


class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        # Bot configuration
        self.BOT_TOKEN = os.getenv("BOT_TOKEN", "")
        
        # LMS API configuration
        self.LMS_API_BASE_URL = os.getenv("LMS_API_BASE_URL", "")
        self.LMS_API_KEY = os.getenv("LMS_API_KEY", "")
        
        # LLM configuration
        self.LLM_API_KEY = os.getenv("LLM_API_KEY", "")
        self.LLM_API_BASE_URL = os.getenv("LLM_API_BASE_URL", "")
        self.LLM_API_MODEL = os.getenv("LLM_API_MODEL", "")


# Global settings instance
settings = Settings()
