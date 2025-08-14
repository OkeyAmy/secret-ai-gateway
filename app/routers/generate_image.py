from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

router = APIRouter()

class ImageGenerateRequest(BaseModel):
    prompt: str
    model: Optional[str] = "models/imagen-4.0-generate-preview-06-06"

@router.post("/generate/image", tags=["Generation"])
async def generate_image(request: ImageGenerateRequest):
    try:
        from app.main import get_gemini_client
        client = get_gemini_client()

        result = client.models.generate_images(
            model=request.model or "models/imagen-4.0-generate-preview-06-06",
            prompt=request.prompt,
            config=dict(
                number_of_images=1,
                output_mime_type="image/jpeg",
                aspect_ratio="1:1",
            ),
        )

        if not getattr(result, 'generated_images', None):
            return {"response": "No images generated."}

        # Return the first image info similar to chat format
        generated_image = result.generated_images[0]
        img = getattr(generated_image, 'image', None)
        if not img:
            return {"response": "No image payload returned."}

        uri = getattr(img, 'uri', None)
        if uri:
            return {"response": uri}

        data = getattr(img, 'bytes', None)
        if data:
            import base64
            return {"response": base64.b64encode(data).decode('utf-8')}

        return {"response": "Image generated, but no URI or data available."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")