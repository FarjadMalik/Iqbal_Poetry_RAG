"""Error handling utilities."""

import logging

logger = logging.getLogger(__name__)

def handle_rag_error(func):
    """Decorator for handling RAG system errors."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in RAG system: {str(e)}")
            return f"An error occurred: {str(e)}", []
    return wrapper
