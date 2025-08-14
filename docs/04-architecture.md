# Architecture Overview

## Components
- `app/main.py`: FastAPI app factory, middleware, error handling, and router wiring. Exposes a lazily-initialized Gemini client via `get_gemini_client()` using API key from env. Uses Gemini API v1beta.
- `app/routers/*.py`: Route modules separated by responsibility:
  - `chat.py`: Text chat endpoint
  - `generate_text.py`: Text generation POST
  - `generate_image.py`: Image generation GET (streams to server file, returns URL)
  - `model.py`: Lists models and categories
  - `health.py`: Health status
  - `files.py`: Serves generated files from `/tmp/ai-images`
- `app/models.py`: Pydantic and enum definitions for request/response and model names
- `app/config.py`: Basic settings

## Data flow
- Requests are received by FastAPI and routed to the appropriate handler.
- Handlers call `get_gemini_client()` when needed, which returns a cached `genai.Client` configured for v1beta.
- For image generation, streaming chunks are examined to find the first inline image; bytes are persisted to `/tmp/ai-images` and a public URL is returned.

## Key decisions
- Keep REST shapes simple and consistent (`{ "response": ... }`).
- Prefer GET for idempotent generation where possible (image) to ease integration.
- Return URLs for large binary outputs (images) rather than embedding base64 in JSON responses.