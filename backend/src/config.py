import os

from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st

    if "OLLAMA_API_KEY" in st.secrets:
        os.environ["OLLAMA_API_KEY"] = st.secrets["OLLAMA_API_KEY"]

    if "OLLAMA_MODEL" in st.secrets:
        os.environ["OLLAMA_MODEL"] = st.secrets["OLLAMA_MODEL"]

except Exception:
    pass

ollama_api_key = os.getenv("OLLAMA_API_KEY")
ollama_model = os.getenv("OLLAMA_MODEL")