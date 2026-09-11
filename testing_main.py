import os

from dotenv import load_dotenv
from ollama import Client


load_dotenv()

api_key = os.getenv("OLLAMA_API_KEY")
model = os.getenv("OLLAMA_MODEL")

if not api_key:
    raise ValueError("OLLAMA_API_KEY not found in .env")

if not model:
    raise ValueError("OLLAMA_MODEL not found in .env")


client = Client(
    host="https://ollama.com",
    headers={
        "Authorization": f"Bearer {api_key}"
    }
)


response = client.chat(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: Ollama connection successful."
        }
    ],
)


print(response.message.content)

