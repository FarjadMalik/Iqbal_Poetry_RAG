"""Embedding functionality for the RAG system."""

import os
from langchain_ollama import OllamaEmbeddings
from app.config import EMBEDDING_MODEL

def get_embeddings():
    """Initialize and return the embedding model."""
    try:
        return OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url="http://localhost:11434"  # Explicitly set the base URL
        )
    except Exception as e:
        print(f"Warning: Failed to initialize OllamaEmbeddings: {e}")
        # Fallback to a different embedding method if needed
        raise
