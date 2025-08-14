# API Reference

Base URL: `https://secret-ai-gateway.onrender.com`

## Health
- GET `/api/health`
- Example:
```bash
curl -s "https://secret-ai-gateway.onrender.com/api/health"
```

## Models
- GET `/api/models`
- Example:
```bash
curl -s "https://secret-ai-gateway.onrender.com/api/models"
```
- Returns:
  - `models`: string[] of model names
  - `model_details`: map of name -> metadata
  - `categories`: { text: string[], image: string[], video: string[] }

## Chat (Text)
- GET `/api/chat`
- Query params:
  - `prompt` (string, required)
  - `model` (enum, optional): `gemini-2.5-flash` (default), `gemini-2.5-pro`, `gemini-2.0-flash`
- Example:
```bash
curl -s "https://secret-ai-gateway.onrender.com/api/chat?prompt=Hello%20Gemini&model=gemini-2.5-flash"
```
- Response examples:
  - `{ "response": "Hello!" }`
  - `{ "Think Process": "...", "Response": "..." }`

## Improve Prompt
- GET `/api/improve-prompt`
- Query params:
  - `prompt` (string, required): prompt to improve
  - `target` (enum, optional): `text` (default) or `image`
- Example (text target):
```bash
curl -s "https://secret-ai-gateway.onrender.com/api/improve-prompt?prompt=Write%20a%20project%20plan&target=text"
```
- Example (image target):
```bash
curl -s "https://secret-ai-gateway.onrender.com/api/improve-prompt?prompt=A%20futuristic%20cityscape&target=image"
```
- Response: `{ "response": "<improved prompt>" }`
- POST `/api/improve-prompt` (Backwards compatible)
  - Body: `{ "prompt": "...", "target": "text|image" }`

## Generate Text (Deprecated)
- DEPRECATED: Use `GET /api/chat` instead for text generation.
- POST `/api/generate/text`
- JSON body:
  - `prompt` (string, required)
  - `model` (string, optional; default `gemini-2.5-flash` or full `models/gemini-2.5-flash`)
- Example:
```bash
curl -s -X POST "https://secret-ai-gateway.onrender.com/api/generate/text" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Write a product tagline","model":"gemini-2.5-flash"}'
```
- Response:
  - `{ "response": "..." }`

## Generate Image
- GET `/api/generate/image`
- Query params:
  - `prompt` (string, required)
  - `model` (string, optional; default `gemini-2.0-flash-preview-image-generation`)
    - allowed: `gemini-2.0-flash-exp-image-generation`, `gemini-2.0-flash-preview-image-generation`
- Example:
```bash
curl -s "https://secret-ai-gateway.onrender.com/api/generate/image?prompt=A%20sunset%20over%20mountains&model=gemini-2.0-flash-preview-image-generation"
```
- Behavior: streams, saves first image as a server file, returns URL
- Response:
  - `{ "response": "https://secret-ai-gateway.onrender.com/api/files/<filename>" }`

## Files
- GET `/api/files/{filename}`
- Example:
```bash
curl -sLO "https://secret-ai-gateway.onrender.com/api/files/<filename>"
```
- Serves generated files stored under `/tmp/ai-images`