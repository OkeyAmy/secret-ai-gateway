from fastapi import HTTPException, Request
from app.config import settings
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# No authorization needed
# API key is managed internally
# Prioritize .env file API key, fallback to hardcoded key
SECRET_AI_API_KEY = os.getenv('SECRET_AI_API_KEY', "bWFzdGVyQHNjcnRsYWJzLmNvbTpTZWNyZXROZXR3b3JrTWFzdGVyS2V5X18yMDI1")