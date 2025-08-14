import os
from google import genai

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

model = "gemini-2.5-flash"

contents = [
    "You are a helpful assistant that translates English to French.",
    "Translate: I love programming."
]

response = client.models.generate_content(
    model=model,
    contents="\n\n".join(contents)
)
print(getattr(response, 'text', str(response)))