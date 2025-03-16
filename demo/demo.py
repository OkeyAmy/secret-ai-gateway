import os
from secret_ai_sdk.secret_ai import ChatSecret
from secret_ai_sdk.secret import Secret

# Initialize the Secret client
secret_client = Secret()

# Get all models registered with the smart contracts
models = secret_client.get_models()

# For your chosen model, get a list of LLM instance URLs
urls = secret_client.get_urls(model=models[0])

# Create the AI client with specific parameters
secret_ai_llm = ChatSecret(
    base_url=urls[0],  # Choose a specific URL
    model=models[0],    # Your selected model
    temperature=1.0
)

# Define your messages
messages = [
    ("system", "You are a helpful assistant that translates English to French."),
    ("human", "I love programming."),
]

# Invoke the LLM (with streaming disabled)
response = secret_ai_llm.invoke(messages, stream=False)
print(response.content)
print(urls)
print(models)