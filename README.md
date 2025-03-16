# Secret Network AI Hub API

![Secret Network](https://th.bing.com/th/id/OIP.Q3YYqq7bTMLB5c__FisPagHaB2?rs=1&pid=ImgDetMain)

## Overview

The Secret Network AI Hub API is a powerful gateway to leverage Secret Network's advanced AI models in your applications. This API provides secure and private access to state-of-the-art language models including DeepSeek R1 (70B) and Llama 3.2 Vision, all running on the privacy-focused Secret Network blockchain infrastructure.

## Key Features

- **🤖 Advanced AI Models**: Access to DeepSeek R1 (70B) and Llama 3.2 Vision models
- **🔒 Privacy-Focused**: Built on Secret Network's privacy-preserving blockchain infrastructure
- **💬 Conversational AI**: Maintain chat sessions with context awareness
- **✨ Prompt Engineering**: Tools to improve and optimize AI prompts
- **🔄 RESTful API**: Simple integration with any application using standard REST endpoints
- **📚 Comprehensive Documentation**: Detailed API documentation via Swagger UI and ReDoc

## Prerequisites

- Python 3.12.0
- Secret AI API Key

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

## Deployment on Render

This project is set up for seamless deployment on Render with the API key pre-configured.

### Automatic Deployment

The easiest way to deploy is to use the included `render.yaml` file:

1. Create a new Render account or sign in at [dashboard.render.com](https://dashboard.render.com)
2. Click on the "New +" button and select "Blueprint"
3. Connect your GitHub/GitLab account and select your repository
4. Render will automatically detect the `render.yaml` file and set up your service
5. The environment variables, including the Secret AI API key, are already configured in the `render.yaml` file

### Manual Deployment

If you prefer to set up manually:

1. Create a new Web Service on Render
2. Connect to your repository
3. Use the following settings:
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add the environment variable:
   - Key: `SECRET_AI_API_KEY`
   - Value: `bWFzdGVyQHNjcnRsYWJzLmNvbTpTZWNyZXROZXR3b3JrTWFzdGVyS2V5X18yMDI1`

The API will be available at your Render URL once deployment is complete.

## Special Note for Frontend Engineers

This API has been configured for easy integration with frontend applications:

### Open Access API

For maximum convenience, this API is configured to accept requests from any origin without requiring authentication:

1. **No API Keys Required** - Frontend applications can make API calls without including any API keys or tokens.

2. **Simple Integration** - Just make standard fetch/axios calls from your frontend application:

```javascript
async function callSecretAI(prompt) {
  const response = await fetch('https://your-render-url.onrender.com/api/chat?prompt=' + encodeURIComponent(prompt));
  return await response.json();
}
```

## Security Note

The API is now configured with an internal API key, eliminating the need for external authentication:

- No API key authentication required
- Simplified integration for frontend and backend applications
- API key managed internally within the application

```javascript
async function callSecretAI(prompt) {
  const response = await fetch('https://your-render-url.onrender.com/api/chat?prompt=' + encodeURIComponent(prompt));
  return await response.json();
}
```

### Deployment Considerations

When deploying, ensure the internal API key is securely managed within your application environment.

## Configuration

| Variable           | Description                                 | Default                        |
|--------------------|---------------------------------------------|--------------------------------|
| CORS_ORIGINS       | Allowed origins for CORS                    | ["*"] (All origins)           |
| ENVIRONMENT        | Current environment (production/dev)        | production                     |

## Project Structure

```
secret-network-ai-api/
├── app/
│   ├── __init__.py
│   ├── config.py         # Application configuration
│   ├── main.py           # Application entry point
│   ├── models.py         # Pydantic models
│   ├── security.py       # API security mechanisms
│   └── routers/          # API route handlers
│       ├── __init__.py
│       ├── chat.py       # Chat endpoint
│       ├── health.py     # Health check endpoint 
│       ├── model.py      # Model information endpoints
│       └── prompt_improver.py # Prompt improvement endpoint
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Dependencies

The key dependencies include:

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management
- **Secret AI SDK**: Official SDK for interacting with Secret Network AI models
- **Uvicorn**: ASGI server implementation for running the API

For a complete list, refer to the `requirements.txt` file.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and further information about Secret Network's AI capabilities, visit [Secret Network](https://docs.scrt.network/secret-network-documentation/secret-ai/introduction).

## Special Thanks

This project was created with love from Windsurf and Secret AI for their project. 

> **Note about API Keys:** The API key is open and publicly available. You can find it in the [Secret AI documentation](https://docs.scrt.network/secret-network-documentation/secret-ai/sdk/setting-up-your-environment).

---

 2025 Secret Network AI Hub | Built with ❤️ by the Secret Network Community
