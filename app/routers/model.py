from fastapi import APIRouter, HTTPException
from app.config import settings
from typing import Dict, Any, List
import os
import requests

router = APIRouter()

@router.get("/models", tags=["Models"])
async def get_available_models():
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GOOGLE_API_KEY is not set")

        url = "https://generativelanguage.googleapis.com/v1beta/models"
        headers = {"x-goog-api-key": api_key}
        params = {"pageSize": 200}
        response = requests.get(url, headers=headers, params=params, timeout=20)
        if not response.ok:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        data = response.json()
        raw_models: List[Dict[str, Any]] = data.get("models", [])

        model_details: Dict[str, Dict[str, Any]] = {}
        model_names: List[str] = []
        for m in raw_models:
            name = m.get("name")
            if not name:
                continue
            item = {
                "name": name,
                "display_name": m.get("displayName") or m.get("display_name"),
                "description": m.get("description"),
                "input_token_limit": m.get("inputTokenLimit") or m.get("input_token_limit"),
                "output_token_limit": m.get("outputTokenLimit") or m.get("output_token_limit"),
                "supported_generation_methods": m.get("supportedGenerationMethods") or m.get("supported_generation_methods"),
                "version": m.get("version"),
                "inference_type": m.get("inferenceType") or m.get("inference_type"),
            }
            model_names.add(name) if hasattr(model_names, 'add') else model_names.append(name)
            model_details[name] = {k: v for k, v in item.items() if v is not None}

        return {
            "models": model_names,
            "model_details": model_details
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving models: {str(e)}")