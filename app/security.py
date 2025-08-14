from fastapi import HTTPException, Request
from app.config import settings
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# No authorization needed
# API key is managed internally
# Google Gemini API key (no default)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')