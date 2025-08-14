from fastapi import APIRouter, HTTPException
from app.config import settings
from datetime import datetime
from uuid import uuid5, NAMESPACE_DNS
from typing import Dict, List, Any, Optional
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
        
        system_prompt = """You are a thoughtful and helpful assistant when hlps user's whith their prompt/question. When answering user questions:
1. Take time to think carefully about the question
2. Consider multiple perspectives and approaches
3. Provide accurate, relevant, and complete information
4. Ensure your responses are clear and easy to understand
5. If you're uncertain about something, acknowledge it transparently
6. Use examples when it helps clarify your explanations
7. Remember previous parts of the conversation to maintain context
8. Ask clarifying questions if the user's request is ambiguous
9. You only respond to user with an appropiate response
Your goal is to provide the most helpful and satisfying response possible, ensuring the user's needs are fully addressed."""

        messages = chat_sessions.get(session_id, [("system", system_prompt)])
        if len(messages) == 0:
            messages.append(("system", system_prompt))
        messages.append(("user", prompt))
        
        # Prepare a single concatenated content for Gemini
        contents = f"{system_prompt}\n\nUser: {prompt}"
        response = gemini_client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=contents
        )
        content = getattr(response, 'text', str(response))
        messages.append(("assistant", content))
        chat_sessions[session_id] = messages
        
        # Parse for think tags if present; otherwise return full response
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

# New request schemas for multimodal chats
class TextChatRequest(BaseModel):
    prompt: str
    model: Optional[str] = "models/gemini-2.5-flash"

class ImageChatRequest(BaseModel):
    prompt: str
    image_base64: Optional[str] = None
    image_url: Optional[str] = None
    mime_type: Optional[str] = "image/png"
    model: Optional[str] = "models/imagen-3.0-generate-002"

class VideoChatRequest(BaseModel):
    prompt: str
    video_base64: Optional[str] = None
    video_url: Optional[str] = None
    mime_type: Optional[str] = "video/mp4"
    model: Optional[str] = "models/veo-3.0-generate-preview"


def _fetch_and_base64(url: str) -> str:
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return base64.b64encode(resp.content).decode("utf-8")

@router.post("/chat/text", tags=['Generation'])
async def chat_text(request: TextChatRequest):
    try:
        from app.main import get_gemini_client
        gemini_client = get_gemini_client()

        contents = f"User: {request.prompt}"
        response = gemini_client.models.generate_content(
            model=request.model or "models/gemini-2.5-flash",
            contents=contents
        )
        content = getattr(response, 'text', str(response))
        return {"response": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error chatting with text model: {str(e)}")

@router.post("/chat/image", tags=['Generation'])
async def chat_image(request: ImageChatRequest):
    try:
        from app.main import get_gemini_client
        gemini_client = get_gemini_client()

        parts: List[Dict[str, Any]] = [{"text": request.prompt}]
        data_b64 = request.image_base64
        if not data_b64 and request.image_url:
            data_b64 = _fetch_and_base64(request.image_url)
        if data_b64:
            parts.append({"inline_data": {"mime_type": request.mime_type or "image/png", "data": data_b64}})

        contents = [
            {
                "role": "user",
                "parts": parts,
            }
        ]
        response = gemini_client.models.generate_content(
            model=request.model or "models/imagen-3.0-generate-002",
            contents=contents,
            generation_config={"response_mime_type": request.mime_type or "image/png"}
        )
        # For image outputs, some models return inline_data; fall back to text
        result = getattr(response, 'text', None)
        if not result and hasattr(response, 'candidates'):
            try:
                parts = response.candidates[0].content.parts
                for p in parts:
                    if hasattr(p, 'inline_data') and getattr(p.inline_data, 'data', None):
                        return {"mime_type": getattr(p.inline_data, 'mime_type', request.mime_type), "data": p.inline_data.data}
            except Exception:
                pass
        return {"response": result or str(response)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error chatting with image model: {str(e)}")

@router.post("/chat/video", tags=['Generation'])
async def chat_video(request: VideoChatRequest):
    try:
        from app.main import get_gemini_client
        gemini_client = get_gemini_client()

        parts: List[Dict[str, Any]] = [{"text": request.prompt}]
        data_b64 = request.video_base64
        if not data_b64 and request.video_url:
            data_b64 = _fetch_and_base64(request.video_url)
        if data_b64:
            parts.append({"inline_data": {"mime_type": request.mime_type or "video/mp4", "data": data_b64}})

        contents = [
            {
                "role": "user",
                "parts": parts,
            }
        ]
        response = gemini_client.models.generate_content(
            model=request.model or "models/veo-3.0-generate-preview",
            contents=contents,
            generation_config={"response_mime_type": request.mime_type or "video/mp4"}
        )
        # Video models may return long-running operations or URIs; return raw payload if text is absent
        result = getattr(response, 'text', None)
        return {"response": result or str(response)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error chatting with video model: {str(e)}")