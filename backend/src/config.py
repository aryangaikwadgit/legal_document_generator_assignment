import os

from dotenv import load_dotenv

load_dotenv()

ollama_api_key = os.getenv("OLLAMA_API_KEY")
ollama_model = os.getenv("OLLAMA_MODEL")

try:
    import streamlit as st

    if st.secrets.get("OLLAMA_API_KEY"):
        ollama_api_key = st.secrets["OLLAMA_API_KEY"]

    if st.secrets.get("OLLAMA_MODEL"):
        ollama_model = st.secrets["OLLAMA_MODEL"]
except Exception:
    pass