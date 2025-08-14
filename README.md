# Gemini AI Gateway API

![Gemini](https://developers.google.com/static/ai/images/gemini-icon.png)

## Overview

This API provides a clean gateway to Google Gemini models for text chat and image generation. It exposes simple REST endpoints so developers can integrate quickly, while remaining understandable to non-developers.

- **Text Chat**: `/api/chat`, `/api/generate/text`
- **Image Generation**: `/api/generate/image`
- **Models Listing**: `/api/models` (includes categories for text, image)
- **Health & Files**: `/api/health`, `/api/files/{filename}`

Read the full documentation in the `docs/` folder:
- Getting started: `docs/01-quickstart.md`
- API usage: `docs/02-api-reference.md`
- Model selection: `docs/03-models-and-categories.md`
- Architecture overview: `docs/04-architecture.md`
- Deployment guide: `docs/05-deployment.md`

## Prerequisites

- Python 3.12.0
- A Google Gemini API key (set `GEMINI_API_KEY` or `GOOGLE_API_KEY`)

## Installation

```bash
# Clone the repository
git clone https://github.com/OkeyAmy/secret-network-ai-api.git
cd secret-network-ai

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
# Windows PowerShell
$env:SECRET_AI_API_KEY="your_api_key_here"

# Windows CMD
set SECRET_AI_API_KEY=your_api_key_here

# Linux/Mac
export SECRET_AI_API_KEY="your_api_key_here"
```

## API Key Information

**Note:** The current API key is publicly available on the Secret Network documentation: 
[Secret Network AI SDK Environment Setup](https://docs.scrt.network/secret-network-documentation/secret-ai/sdk/setting-up-your-environment)

### Future-Proofing API Key

In case the API key changes or you want to use a personal key:
1. Create a `.env` file in the project root
2. Add your personal API key:
   ```
   SECRET_AI_API_KEY=your_new_api_key_here
   ```
3. The application will automatically use your custom API key if provided

## API Key Configuration

### Using a Personal API Key

If you want to use your own Secret Network AI API key:

1. Create a `.env` file in the project root directory
2. Add your API key to the `.env` file:

```
SECRET_AI_API_KEY=your_personal_api_key_here
```

The API will automatically prioritize your personal API key from the `.env` file over the default key.

#### Obtaining an API Key

You can find the API key details at: [Secret Network AI Documentation](https://docs.scrt.network/secret-network-documentation/secret-ai/sdk/setting-up-your-environment)

### Installation Requirements

To use the `.env` file, ensure you have the `python-dotenv` package installed:

```bash
pip install python-dotenv
```

### Security Considerations

- Do not commit the `.env` file to version control
- Add `.env` to your `.gitignore` file
- Keep your API key confidential

## Running the API

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Models

- `GET /api/models` - Get available AI models

### Chat

- `GET /api/chat` - Chat with an AI model
  - Parameters:
    - `prompt`: The user's question or prompt
    - `model`: (Optional) The AI model to use

### Prompt Improvement

- `POST /api/improve-prompt` - Analyze and improve a user-provided prompt
  - Body:
    - `prompt`: The prompt text to improve

### Health Check

- `GET /api/health` - Check the health status of the API

## Usage Examples

### Chat with AI Model

```python
import requests

BASE_URL = "http://localhost:8000"

response = requests.get(
    f"{BASE_URL}/api/chat",
    params={
        "prompt": "Explain the benefits of Secret Network for AI applications",
        "model": "deepseek-r1:70b"
    }
)

print(response.json())
```

### Improve a Prompt

```python
import requests

BASE_URL = "http://localhost:8000"

data = {
    "prompt": "Write a story about artificial intelligence"
}

response = requests.post(
    f"{BASE_URL}/api/improve-prompt",
    json=data
)

print(response.json())
```

### Get Available Models

```python
import requests

BASE_URL = "http://localhost:8000"

response = requests.get(f"{BASE_URL}/api/models")
print(response.json())
```