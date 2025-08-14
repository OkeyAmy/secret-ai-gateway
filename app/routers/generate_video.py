from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import time

router = APIRouter()

class VideoGenerateRequest(BaseModel):
    prompt: str
    model: Optional[str] = "models/veo-3.0-generate-preview"
    aspect_ratio: str = "16:9"
    number_of_videos: int = 1
    duration_seconds: int = 8
    person_generation: str = "ALLOW_ALL"
    wait: bool = True
    poll_interval_seconds: int = 10
    timeout_seconds: int = 180

@router.post("/generate/video", tags=["Generation"])
async def generate_video(request: VideoGenerateRequest):
    try:
        from app.main import get_gemini_client
        from google.genai import types
        client = get_gemini_client()

        video_config = types.GenerateVideosConfig(
            aspect_ratio=request.aspect_ratio,
            number_of_videos=request.number_of_videos,
            duration_seconds=request.duration_seconds,
            person_generation=request.person_generation,
        )

        operation = client.models.generate_videos(
            model=request.model or "models/veo-3.0-generate-preview",
            prompt=request.prompt,
            config=video_config,
        )

        if not request.wait:
            # Return operation handle for client-side polling
            return {"operation": getattr(operation, 'name', str(operation))}

        # Poll until done or timeout
        start = time.time()
        while not getattr(operation, 'done', False):
            if time.time() - start > request.timeout_seconds:
                return {
                    "status": "timeout",
                    "operation": getattr(operation, 'name', str(operation))
                }
            time.sleep(max(1, request.poll_interval_seconds))
            operation = client.operations.get(operation)

        result = getattr(operation, 'result', None)
        if not result:
            return {"videos": []}

        videos: List[Dict[str, Any]] = []
        for generated_video in getattr(result, 'generated_videos', []) or []:
            vid = getattr(generated_video, 'video', None)
            if not vid:
                continue
            entry: Dict[str, Any] = {}
            uri = getattr(vid, 'uri', None)
            if uri:
                entry['uri'] = uri
            mime = getattr(vid, 'mime_type', None)
            if mime:
                entry['mime_type'] = mime
            videos.append(entry)

        return {"videos": videos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating video: {str(e)}")