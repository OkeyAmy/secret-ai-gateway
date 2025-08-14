# Quickstart

This guide helps you get up and running quickly with the Gemini AI Gateway API.

## Hosted Base URL
- `https://secret-ai-gateway.onrender.com/`

## Requirements
- Python 3.12+
- A Gemini API key set as `GEMINI_API_KEY` (or `GOOGLE_API_KEY`)

## Install and run (local)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Health check
```bash
curl -s "https://secret-ai-gateway.onrender.com/api/health"
```

## List models
```bash
curl -s "https://secret-ai-gateway.onrender.com/api/models"
```

## Chat (text)
```bash
curl -s "https://secret-ai-gateway.onrender.com/api/chat?prompt=Hello%20Gemini&model=gemini-2.5-flash"
```

## Generate image (GET)
Returns a URL to the generated image file.
```bash
curl -s "https://secret-ai-gateway.onrender.com/api/generate/image?prompt=A%20sunset&model=gemini-2.0-flash-preview-image-generation"
```