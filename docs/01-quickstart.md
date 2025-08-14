# Quickstart

This guide helps you get up and running quickly with the Gemini AI Gateway API.

## Requirements
- Python 3.12+
- A Gemini API key set as `GEMINI_API_KEY` (or `GOOGLE_API_KEY`)

## Install and run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Health check
```bash
curl -s "http://localhost:8000/api/health"
```

## List models
```bash
curl -s "http://localhost:8000/api/models"
```

## Chat (text)
```bash
curl -s "http://localhost:8000/api/chat?prompt=Hello%20Gemini&model=gemini-2.5-flash"
```

## Generate text
```bash
curl -s -X POST "http://localhost:8000/api/generate/text" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Write a short poem","model":"gemini-2.5-flash"}'
```

## Generate image (GET)
The image endpoint streams, saves the first result, and returns a URL.
```bash
curl -s "http://localhost:8000/api/generate/image?prompt=A%20sunset&model=gemini-2.0-flash-preview-image-generation"
```
The response contains a `response` URL you can open in a browser.