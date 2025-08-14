# API Reference

Base URL: `https://secret-ai-gateway.onrender.com`

## Health
- GET `/api/health`
- Returns service status

## Models
- GET `/api/models`
- Returns:
  - `models`: string[] of model names
  - `model_details`: map of name -> metadata
  - `categories`: { text: string[], image: string[], video: string[] }

## Chat (Text)
- GET `/api/chat`
- Query params:
  - `prompt` (string, required)
  - `model` (enum, optional): `gemini-2.5-flash` (default), `gemini-2.5-pro`, `gemini-2.0-flash`
- Response examples:
  - `{ "response": "Hello!" }`
  - `{ "Think Process": "...", "Response": "..." }`

## Generate Text
- POST `/api/generate/text`
- JSON body:
  - `prompt` (string, required)
  - `model` (string, optional; default `gemini-2.5-flash` or full `models/gemini-2.5-flash`)
- Response:
  - `{ "response": "..." }`

## Generate Image
- GET `/api/generate/image`
- Query params:
  - `prompt` (string, required)
  - `model` (string, optional; default `gemini-2.0-flash-preview-image-generation`)
    - allowed: `gemini-2.0-flash-exp-image-generation`, `gemini-2.0-flash-preview-image-generation`
- Behavior: streams, saves first image as a server file, returns URL
- Response:
  - `{ "response": "https://secret-ai-gateway.onrender.com/api/files/<filename>" }`

## Files
- GET `/api/files/{filename}`
- Serves generated files stored under `/tmp/ai-images`