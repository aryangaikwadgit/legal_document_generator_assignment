import os

from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
    ollama_api_key = st.secrets.get("OLLAMA_API_KEY")
    ollama_model = st.secrets.get("OLLAMA_MODEL")
except Exception:
    ollama_api_key = os.getenv("OLLAMA_API_KEY")
    ollama_model = os.getenv("OLLAMA_MODEL")