from enum import Enum
from pydantic import BaseModel
from typing import Optional  # Add this import

class AvailableModels(str, Enum):
    GEMINI_FLASH = "gemini-2.5-flash"
    GEMINI_PRO = "gemini-2.5-pro"
    GEMINI_FLASH_20 = "gemini-2.0-flash"

class GenerateRequest(BaseModel):
    prompt: str  
    image: Optional[str] = None  
    session_id: Optional[str] = None