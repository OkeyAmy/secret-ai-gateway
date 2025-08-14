from fastapi import APIRouter, HTTPException
from app.config import settings
from typing import Dict, Any

router = APIRouter()

@router.get("/models", tags=["Models"])
async def get_available_models():
	try:
		models = ["gemini-2.5-flash"]
		model_info = {
			"gemini-2.5-flash": {
				"description": "Google Gemini 2.5 Flash: fast, cost-efficient multimodal model",
				"capabilities": ["text generation", "multimodal input", "function calling", "structured outputs"],
				"max_input_tokens": 1048576,
				"max_output_tokens": 65536,
				"recommended_temperature": 0.7
			}
		}
		return {
			"models": models,
			"model_details": {model: model_info.get(model, {}) for model in models}
		}
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Error retrieving models: {str(e)}")