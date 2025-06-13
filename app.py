"""Entry point for the Iqbal Poetry RAG application."""

import os
import sys
import requests
import subprocess
from interface.RAGSystem import IqbalRAGSystem
from interface.gradio_interface import launch_gradio_app
from interface.config import JSON_FILE_PATH

def check_ollama_availability():
    """Check if Ollama is running and has the required models."""
    try:
        # First check if Ollama service is running
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        
        if response.status_code == 200:
            # Check available models
            available_models = [model["name"].lower() for model in response.json().get("models", [])]
            
            if "llama3" not in available_models:
                print("Warning: llama3 model not found in Ollama.")
                # Try to check again with list command
                try:
                    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
                    if "llama3" in result.stdout.lower():
                        print("Model found via command line. Proceeding...")
                        return True
                    else:
                        print("Please install it with: ollama pull llama3")
                        return False
                except Exception:
                    print("Could not check models via command line.")
                    return False
            return True
        else:
            print(f"Warning: Ollama is running but API call failed with status {response.status_code}.")
            return False
    except requests.exceptions.ConnectionError:
        print("Error: Ollama server is not running. Please start Ollama with:")
        print("ollama serve")
        return False
    except Exception as e:
        print(f"Error checking Ollama: {str(e)}")
        return False

def check_data_file():
    """Check if the required data file exists."""
    if not os.path.exists(JSON_FILE_PATH):
        print(f"Error: Required data file not found at {JSON_FILE_PATH}")
        print("Please ensure the iqbal_poems_rag.json file is present in the data/processed_data directory.")
        return False
    return True

if __name__ == "__main__":
    # Check if data file exists
    if not check_data_file():
        sys.exit(1)
    
    # Check if Ollama is available
    ollama_available = check_ollama_availability()
    if not ollama_available:
        print("Warning: Proceeding without verifying Ollama setup...")
    
    try:
        # Initialize RAG system (this will build the vector store if needed)
        print("Initializing Iqbal Poetry RAG system...")
        rag_system = IqbalRAGSystem()
        
        # Launch Gradio app
        print("Launching Gradio interface...")
        print(f"Access the application at http://localhost:{os.getenv('PORT', 7860)}")
        launch_gradio_app(system=rag_system)
    except Exception as e:
        print(f"Error: Failed to start the application: {str(e)}")
        sys.exit(1)
