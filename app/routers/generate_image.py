from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from google.genai import types
import base64
import mimetypes

router = APIRouter()

ALLOWED_IMAGE_MODELS = {
    "models/gemini-2.0-flash-exp-image-generation",
    "models/gemini-2.0-flash-preview-image-generation",
}

class ImageGenerateRequest(BaseModel):
    prompt: str
    model: Optional[str] = "models/gemini-2.0-flash-preview-image-generation"

def _generate_image_stream(prompt: str, model: str) -> Dict[str, Any]:
    if model not in ALLOWED_IMAGE_MODELS:
        raise HTTPException(status_code=400, detail="Unsupported image model. Use one of: gemini-2.0-flash-exp-image-generation or gemini-2.0-flash-preview-image-generation")
    from app.main import get_gemini_client
    client = get_gemini_client()

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )
    ]
    config = types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
    )

    first_image_b64: Optional[str] = None
    first_image_mime: Optional[str] = None
    first_text: Optional[str] = None

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        try:
            if not chunk.candidates:
                continue
            content = chunk.candidates[0].content
            if not content or not content.parts:
                continue
            part = content.parts[0]
            if getattr(part, "inline_data", None) and getattr(part.inline_data, "data", None):
                # Capture first image
                if first_image_b64 is None:
                    first_image_b64 = part.inline_data.data
                    first_image_mime = getattr(part.inline_data, "mime_type", None)
            else:
                # Capture first text chunk
                if first_text is None and hasattr(chunk, "text") and chunk.text:
                    first_text = chunk.text
        except Exception:
            continue

    if first_image_b64 is not None:
        # Return base64 as response (chat-like response key)
        prefix = f"data:{first_image_mime};base64," if first_image_mime else ""
        if isinstance(first_image_b64, bytes):
            b64 = base64.b64encode(first_image_b64).decode("utf-8")
        else:
            b64 = first_image_b64
        return {"response": prefix + b64}
    if first_text:
        return {"response": first_text}
    return {"response": "No image generated."}

@router.get("/generate/image", tags=["Generation"])
async def generate_image_get(
    prompt: str = Query(..., description="The prompt to generate an image"),
    model: str = Query("models/gemini-2.0-flash-preview-image-generation", description="Image model to use")
):
    try:
        return _generate_image_stream(prompt=prompt, model=model)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")