from fastapi import APIRouter, HTTPException, Body
from app.config import settings
from pydantic import BaseModel
from typing import Dict, Any
from app.models import AvailableModels

router = APIRouter()
# System prompt for prompt improvement
PROMPT_IMPROVER_SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You improve user prompts to be clear, specific, and goal-oriented."
        " Preserve original intent while making the prompt unambiguous and actionable."
        " Include constraints, success criteria, and short examples when helpful."
        " Use concise language and numbered steps only if they add clarity."
    )
}

class PromptRequest(BaseModel):
    prompt: str

@router.post("/improve-prompt", tags=["Prompt Improvement"])
async def improve_prompt(
    prompt: str = Body(..., description="The prompt text to improve")
) -> dict:
    try:
        from app.main import get_gemini_client  # Use shared client
        gemini_client = get_gemini_client()
        
        improvement_prompt = f"""Improve the following prompt while preserving intent.
- Remove ambiguity
- Add necessary context and constraints
- Include format or examples only if helpful

USER PROMPT:
{prompt}

Return only the improved prompt, nothing else.
"""
        
        messages = [
            PROMPT_IMPROVER_SYSTEM_PROMPT,
            {"role": "user", "content": improvement_prompt}
        ]

        contents = f"{PROMPT_IMPROVER_SYSTEM_PROMPT['content']}\n\nUser: {improvement_prompt}"
        response = gemini_client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=contents
        )
        content = getattr(response, 'text', str(response))
        
        if "<think>" in content and "</think>" in content:
            try:
                think_start = content.find("<think>") + len("<think>")
                think_end = content.find("</think>")
                think_output = content[think_start:think_end].strip()
                actual_response = content[content.find("</think>") + len("</think>"):].strip()
                return {
                    "Think Process": think_output,
                    "Response": actual_response
                }
            except Exception:
                return {"response": content}
        else:
            return {"response": content}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error improving prompt: {str(e)}"
        )