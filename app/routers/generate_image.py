from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

router = APIRouter()

class ImageGenerateRequest(BaseModel):
    prompt: str
    model: Optional[str] = "models/imagen-3.0-generate-002"
    number_of_images: int = 1
    output_mime_type: str = "image/jpeg"
    aspect_ratio: str = "1:1"
    person_generation: str = "ALLOW_ALL"

@router.post("/generate/image", tags=["Generation"])
async def generate_image(request: ImageGenerateRequest):
    try:
        from app.main import get_gemini_client
        client = get_gemini_client()

        result = client.models.generate_images(
            model=request.model or "models/imagen-3.0-generate-002",
            prompt=request.prompt,
            config=dict(
                number_of_images=request.number_of_images,
                output_mime_type=request.output_mime_type,
                person_generation=request.person_generation,
                aspect_ratio=request.aspect_ratio,
            ),
        )

        if not getattr(result, 'generated_images', None):
            return {"images": []}

        images: List[Dict[str, Any]] = []
        for generated_image in result.generated_images:
            entry: Dict[str, Any] = {}
            img = getattr(generated_image, 'image', None)
            if img is None:
                continue
            # Prefer URI if present
            uri = getattr(img, 'uri', None)
            if uri:
                entry['uri'] = uri
            # Provide base64 if library offers bytes
            data = getattr(img, 'bytes', None)
            if data:
                import base64
                entry['b64'] = base64.b64encode(data).decode('utf-8')
            # Include mime_type if available
            mime = getattr(img, 'mime_type', None)
            if mime:
                entry['mime_type'] = mime
            images.append(entry)

        return {"images": images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")