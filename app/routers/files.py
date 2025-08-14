from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

BASE_DIR = "/tmp/ai-images"

@router.get("/files/{filename}", tags=["Files"])
async def get_file(filename: str):
    try:
        file_path = os.path.join(BASE_DIR, filename)
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(file_path)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving file: {str(e)}")