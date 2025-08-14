from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from google.genai import types
import base64
import mimetypes
import os
import uuid

router = APIRouter()

ALLOWED_IMAGE_MODELS = {
    "gemini-2.0-flash-exp-image-generation",
    "gemini-2.0-flash-preview-image-generation",
}

class ImageGenerateRequest(BaseModel):
    prompt: str
    model: Optional[str] = "gemini-2.0-flash-preview-image-generation"

def _generate_image_stream_to_file(prompt: str, model_name: str) -> Dict[str, Any]:
    if model_name not in ALLOWED_IMAGE_MODELS:
        raise HTTPException(status_code=400, detail="Unsupported image model. Use one of: gemini-2.0-flash-exp-image-generation or gemini-2.0-flash-preview-image-generation")
    full_model = f"models/{model_name}"
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

    first_image_bytes: Optional[bytes] = None
    first_image_mime: Optional[str] = None
    first_text: Optional[str] = None

    for chunk in client.models.generate_content_stream(
        model=full_model,
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
                if first_image_bytes is None:
                    data = part.inline_data.data
                    if isinstance(data, str):
                        try:
                            first_image_bytes = base64.b64decode(data)
                        except Exception:
                            first_image_bytes = data.encode("utf-8")
                    else:
                        first_image_bytes = data
                    first_image_mime = getattr(part.inline_data, "mime_type", None)
            else:
                if first_text is None and hasattr(chunk, "text") and chunk.text:
                    first_text = chunk.text
        except Exception:
            continue

    if first_image_bytes is not None:
        base_dir = "/tmp/ai-images"
        os.makedirs(base_dir, exist_ok=True)
        ext = mimetypes.guess_extension(first_image_mime or "image/jpeg") or ".jpg"
        filename = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(base_dir, filename)
        with open(file_path, "wb") as f:
            f.write(first_image_bytes)
        return {"filename": filename}

    if first_text:
        return {"text": first_text}
    return {"text": "No image generated."}

@router.get("/generate/image", tags=["Generation"])
async def generate_image_get(
    request: Request,
    prompt: str = Query(..., description="The prompt to generate an image"),
    model: str = Query("gemini-2.0-flash-preview-image-generation", description="Image model to use (dropdown of two options)")
):
    try:
        result = _generate_image_stream_to_file(prompt=prompt, model_name=model)
        if "filename" in result:
            url = str(request.base_url) + f"api/files/{result['filename']}"
            return {"response": url}
        else:
            # Fallback text response
            return {"response": result.get("text", "No image generated.")}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")