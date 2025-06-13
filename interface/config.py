"""Configuration settings for the Iqbal Poetry RAG application."""

import os
import gradio as gr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application settings
APP_NAME = "RAG-Iqbal: Q&A with Allama Iqbal based on a poetry dataset"
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

# API Keys
# PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_DB_DIR = os.path.join(BASE_DIR, "outputs", "iqbalchroma_db")
FEEDBACK_DIR = os.path.join(BASE_DIR, "outputs", "feedback")
JSON_FILE_PATH = os.path.join(BASE_DIR, "data", "processed_data", "iqbal_poems_rag.json")

# Create necessary directories
os.makedirs(os.path.dirname(JSON_FILE_PATH), exist_ok=True)
os.makedirs(CHROMA_DB_DIR, exist_ok=True)
os.makedirs(FEEDBACK_DIR, exist_ok=True)

# RAG settings
EMBEDDING_MODEL = "llama3"  # This should match your Ollama model name exactly
LLM_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"   # "microsoft/phi-2"
RETRIEVER_K = 5
RETRIEVER_FETCH_K = 20
RETRIEVER_LAMBDA_MULT = 0.75
SCORE_THRESHOLD = 0.65

# Gradio settings
GRADIO_THEME = gr.themes.Soft()  # Import gr here
GRADIO_SERVER_PORT = int(os.getenv("PORT", 7860))
