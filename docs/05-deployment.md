# Deployment Guide

## Environment
- `GEMINI_API_KEY` or `GOOGLE_API_KEY`: API key for Google Gemini
- Optional CORS: `CORS_ORIGINS` (comma-separated)

## Build & Run (Uvicorn)
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Production tips
- Front a reverse proxy (nginx) for TLS and caching
- Persist `/tmp/ai-images` to a durable storage if you need long-lived URLs
- Add authentication/quotas if exposing publicly
- Monitor logs and set sensible timeouts

## Container
- Create a Dockerfile using a Python 3.12 base image
- Copy code, install requirements, expose 8000, set entrypoint to uvicorn