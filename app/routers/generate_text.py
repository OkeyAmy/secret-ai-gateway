from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class TextGenerateRequest(BaseModel):
    prompt: str
    model: Optional[str] = "models/gemini-2.5-flash"

@router.post("/generate/text", tags=["Generation"])
async def generate_text(request: TextGenerateRequest):
    try:
        from app.main import get_gemini_client
        client = get_gemini_client()
        response = client.models.generate_content(
            model=request.model or "models/gemini-2.5-flash",
            contents=request.prompt
        )
        return {"response": getattr(response, 'text', str(response))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")