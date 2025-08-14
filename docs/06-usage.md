# Usage Guide

This document shows how to integrate the hosted API into your project quickly and safely.

Base URL (Render): `https://secret-ai-gateway.onrender.com`

## Routes overview
- Text chat: `GET /api/chat`
- Generate text: `POST /api/generate/text`
- Generate image: `GET /api/generate/image`
- List models: `GET /api/models`
- Health: `GET /api/health`
- Files: `GET /api/files/{filename}`

## Chat (text)
- Endpoint: `GET /api/chat`
- Params:
  - `prompt` (required): your message
  - `model` (optional): one of `gemini-2.5-flash` (default), `gemini-2.5-pro`, `gemini-2.0-flash`
- Example (JS):
```javascript
const BASE = 'https://secret-ai-gateway.onrender.com';
const q = new URLSearchParams({ prompt: 'Explain WebSockets', model: 'gemini-2.5-pro' });
const res = await fetch(`${BASE}/api/chat?${q.toString()}`);
const data = await res.json();
console.log(data.response ?? data);
```

## Generate text
- Endpoint: `POST /api/generate/text`
- Body:
```json
{
  "prompt": "Summarize the following article...",
  "model": "gemini-2.5-flash"
}
```
- Example (curl):
```bash
curl -s -X POST "https://secret-ai-gateway.onrender.com/api/generate/text" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Write a 1-sentence mission statement","model":"gemini-2.5-flash"}'
```

## Generate image
- Endpoint: `GET /api/generate/image`
- Params:
  - `prompt` (required): image description
  - `model` (optional; default: `gemini-2.0-flash-preview-image-generation`)
    - allowed: `gemini-2.0-flash-exp-image-generation`, `gemini-2.0-flash-preview-image-generation`
- The API streams, saves the first generated image, and returns a URL.
- Example (JS):
```javascript
const BASE = 'https://secret-ai-gateway.onrender.com';
const q = new URLSearchParams({ prompt: 'A cinematic portrait in soft golden hour light', model: 'gemini-2.0-flash-preview-image-generation' });
const res = await fetch(`${BASE}/api/generate/image?${q.toString()}`);
const { response: imageUrl } = await res.json();
// imageUrl is like `${BASE}/api/files/<filename>`
```

## Prompt improver (optional target)
- Endpoint: `POST /api/improve-prompt`
- Body (text target, default):
```json
{
  "prompt": "Write a landing page hero copy for a fintech app",
  "target": "text"
}
```
- Body (image target):
```json
{
  "prompt": "A futuristic cityscape with neon lights and rainy streets",
  "target": "image"
}
```
- Behavior:
  - `text` target returns an improved prompt with title, instructions, constraints, examples (if helpful)
  - `image` target returns an optimized image prompt plus attributes: style, medium, lighting, color palette, camera, aspect ratio, and negatives (optional)

## Model selection (dropdowns)
- Use `GET /api/models` to populate dropdowns. Use `categories.text` for text chat and `categories.image` for image generation.
- For chat, pass short names (e.g., `gemini-2.5-flash`). For image generation, pass one of the allowed short names for image models.

## Frontend tips
- Always render a loading state while calling the API
- Handle `{ response: ... }` uniformly; ensure you display the `response` string or link
- Cache model lists from `/api/models` for session runtime
- For images, display the returned URL directly in an `<img>` tag or download it via `/api/files/{filename}`

## Errors
- The API returns HTTP errors with `{ "detail": "..." }`
- Common issues:
  - Missing API key in backend environment
  - Unsupported model name
  - Network timeouts (retry with backoff)