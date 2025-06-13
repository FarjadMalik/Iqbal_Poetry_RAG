"""Vector store management for the RAG system."""

import json
import os
from langchain_chroma import Chroma  # Updated import
from langchain_core.documents import Document
from interface.config import CHROMA_DB_DIR
from rag.embeddings import get_embeddings

def initialize_vector_store():
    """Initialize and return the Chroma vector store."""
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings
    )

def build_vector_store_from_json(json_file_path):
    """Build and persist a vector store from JSON data."""
    # Check if vector store already exists
    if os.path.exists(CHROMA_DB_DIR) and os.listdir(CHROMA_DB_DIR):
        print(f"Vector store already exists at {CHROMA_DB_DIR}. Skipping creation.")
        return initialize_vector_store()
    
    print(f"Building vector store from {json_file_path}...")
    embeddings = get_embeddings()
    
    # Load JSON data
    with open(json_file_path, 'r', encoding='utf-8') as f:
        poems_data = json.load(f)
    
    # Convert to documents
    documents = []
    for poem in poems_data:
        # Create content with all available information
        content_parts = []
        if poem.get('poem_id'):
            content_parts.append(f"Poem ID: {poem['poem_id']}")
        if poem.get('book_title'):
            content_parts.append(f"Book: {poem['book_title']}")
        if poem.get('full_text'):
            content_parts.append(f"Text:\n{poem['full_text']}")
        
        # Create metadata
        metadata = {
            "poem_id": poem.get("poem_id", ""),
            "book_id": poem.get("book_id", ""),
            "book_title": poem.get("book_title", "Unknown")
        }
        
        # Create document
        doc = Document(
            page_content="\n\n".join(content_parts),
            metadata=metadata
        )
        
        documents.append(doc)
    
    print(f"Creating vector store with {len(documents)} documents...")
    
    # Create vector store
    os.makedirs(CHROMA_DB_DIR, exist_ok=True)
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR
    )
    
    print(f"Vector store created and persisted at {CHROMA_DB_DIR}")
    return vector_store
