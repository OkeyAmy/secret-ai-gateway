from enum import Enum
from pydantic import BaseModel
from typing import Optional  # Add this import

class AvailableModels(str, Enum):
    GEMINI_FLASH = "gemini-2.5-flash"

class GenerateRequest(BaseModel):
    prompt: str  
    image: Optional[str] = None  
    session_id: Optional[str] = None