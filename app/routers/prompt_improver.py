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
        "Role: Expert Prompt Engineer.\n"
        "Goal: Transform user prompts into clear, specific, and effective instructions while preserving intent.\n\n"
        "What to do\n"
        "- Remove ambiguity: replace vague terms with measurable details\n"
        "- Add essential context: audience, objective, constraints, success criteria\n"
        "- Structure output needs: format, sections, bullet lists, examples if helpful\n"
        "- Calibrate tone and length: concise by default; expand only if necessary\n"
        "- Keep it implementable: numbered steps or checklist when appropriate\n\n"
        "What to avoid\n"
        "- Do not change the core intent\n"
        "- Do not add speculative requirements\n"
        "- Do not include meta commentary or explanations in the final output\n\n"
        "Response format\n"
        "Return ONLY the improved prompt, ready to copy‑paste, without extra commentary."
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
        
        improvement_prompt = f"""Improve the following prompt while preserving its intent.
- Remove ambiguity and add essential context and constraints
- Specify format or examples only when they add clarity
- Keep it concise and implementable

USER PROMPT:
{prompt}

Return ONLY the improved prompt, nothing else.
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