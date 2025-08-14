from fastapi import APIRouter, HTTPException
from app.config import settings
from datetime import datetime
from uuid import uuid5, NAMESPACE_DNS
from typing import Dict, List, Any
from app.models import AvailableModels
from pydantic import BaseModel
import base64
import requests

router = APIRouter()

chat_sessions: Dict[str, List[dict]] = {}

@router.get("/chat", tags=['Generation'])
async def chat_with_model(
    prompt: str,
    model: AvailableModels = AvailableModels.GEMINI_FLASH
):
    try:
        from app.main import get_gemini_client
        gemini_client = get_gemini_client()
        
        session_id = f"session_{uuid5(NAMESPACE_DNS, 'default_api_key')}"
        
        system_prompt = (
            "You are a precise, helpful assistant."
            " Always answer clearly, factually, and concisely."
            " If the prompt is ambiguous, ask one brief clarifying question."
            " When relevant, provide short examples or steps."
            " Avoid speculation and include only information you can justify."
        )

        messages = chat_sessions.get(session_id, [("system", system_prompt)])
        if len(messages) == 0:
            messages.append(("system", system_prompt))
        messages.append(("user", prompt))
        
        # Normalize model name to full path
        model_name = model.value
        full_model = model_name if model_name.startswith("models/") else f"models/{model_name}"

        response = gemini_client.models.generate_content(
            model=full_model,
            contents=f"{system_prompt}\n\nUser: {prompt}"
        )
        content = getattr(response, 'text', str(response))
        messages.append(("assistant", content))
        chat_sessions[session_id] = messages
        
        if "<think>" in content and "</think>" in content:
            try:
                think_start = content.find("<think>") + len("<think>")
                think_end = content.find("</think>")
                think_output = content[think_start:think_end].strip()
                actual_response = content[think_end + len("</think>"):].strip()
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
            detail=f"Error chatting with model: {str(e)}"
        )