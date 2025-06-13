"""Retriever configuration for the RAG system."""

from interface.config import RETRIEVER_K, RETRIEVER_FETCH_K, RETRIEVER_LAMBDA_MULT

def configure_retriever(vector_store):
    """Configure and return the retriever."""
    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            'k': RETRIEVER_K,
            'fetch_k': RETRIEVER_FETCH_K,
            'lambda_mult': RETRIEVER_LAMBDA_MULT
        }
    )
