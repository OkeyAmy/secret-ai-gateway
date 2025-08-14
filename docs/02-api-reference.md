# API Reference

Base URL: `http://localhost:8000`

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
  - `model` (enum, optional): `gemini-2.5-flash` (default), `gemini-2.5-pro`, `gemini-2.0-flash`, `gemini-2.0-pro-exp`
- Response examples:
  - `{ "response": "Hello!" }`
  - `{ "Think Process": "...", "Response": "..." }`

## Generate Text
- POST `/api/generate/text`
- JSON body:
  - `prompt` (string, required)
  - `model` (string, optional; default `models/gemini-2.5-flash` allowed as short name `gemini-2.5-flash`)
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
  - `{ "response": "http://localhost:8000/api/files/<filename>" }`

## Files
- GET `/api/files/{filename}`
- Serves generated files stored under `/tmp/ai-images`