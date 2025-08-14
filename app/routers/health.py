from fastapi import APIRouter, HTTPException
import os

router = APIRouter()

@router.get("/health", tags=["System"])
async def health_check():
	try:
		configured = bool(os.getenv("GOOGLE_API_KEY"))
		return {
			"status": "healthy" if configured else "degraded",
			"gemini_api_configuration": "configured" if configured else "missing_key",
			"available_models": 1 if configured else 0,
			"api_version": "1.0.0"
		}
	except Exception as e:
		raise HTTPException(
			status_code=503,
			detail={
				"status": "unhealthy",
				"error": str(e),
				"gemini_api_configuration": "missing"
			}
		)