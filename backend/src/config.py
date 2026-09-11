import os 

from dotenv import load_dotenv

load_dotenv()

ollama_api_key = os.getenv("OLLAMA_API_KEY")

ollama_model = os.getenv("OLLAMA_MODEL")