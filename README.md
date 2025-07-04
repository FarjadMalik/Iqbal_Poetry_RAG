---
title: "Iqbal Poetry RAG System"
emoji: "📜"
colorFrom: "yellow"
colorTo: "purple"
sdk: "gradio"
python_version: "3.10"
start_command: "python app.py"
short_description: "A Gradio RAG app for querying the poetry of Allama Iqbal."
tags:
  - rag
  - poetry
  - gradio
  - iqbal
  - language-models
---

# Iqbal Poetry RAG System

A Retrieval-Augmented Generation (RAG) system for exploring and querying the poetry of Allama Iqbal. This project leverages vector search and large language models (LLMs) to answer questions about Iqbal's poetry, providing relevant poem excerpts as context. 

Note: On first run your will need to set up the vector embeddings store so the set up and initialization can take a few hours dependings on the performance of your PC.

![Teaser image of the system in action](data/Iqbal_Khudi_Teaser.png)

---

## Features

- **Semantic Search**: Retrieve the most relevant poems and their themes for a given question using vector embeddings.
- **LLM-Powered Answers**: Generate answers using a language model, grounded in retrieved poem context.
- **Gradio Interface**: User-friendly web interface powered by [Gradio](https://gradio.app/).
- **Plug-and-Play Dataset**: The poetry dataset is already included in the repository, with all paths set up for immediate use.
- **Configurable**: Easily adjust retrieval thresholds, model settings, and data sources.
- **Error Handling**: Robust error management for smoother user experience.
- **(Optional) Feedback Logging**: Log user feedback for continuous improvement.

---

## Installation

### Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) (a fast Python package installer, drop-in replacement for pip)
- HuggingFace account (https://huggingface.co/) (to use pretrained models)
- Ollama (https://ollama.com/) (to create vector embeddings)

```bash
# install Ollama
curl -sSfL https://ollama.ai/install.sh | sh

# pull a model
ollama pull llama3
```

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/iqbal_poetry_rag.git
cd iqbal_poetry_rag
```

### 2. Install dependencies

```bash
uv pip install -r requirements.txt
```

---

## Usage

**Just plug and run!**  
The poetry dataset is already included in the repository, and all file paths are set up using relative paths. No additional data preparation is required.

To launch the Gradio app locally:

```bash
python app.py
```

This will start a Gradio web interface in your browser, where you can enter your questions about Iqbal's poetry and receive contextually grounded answers.

---

## Project Structure

```
iqbal_poetry_rag/
│
├── interface/
│   ├── RAGSystem.py          # Main RAG system class
│   ├── gradio_interface.py   # Gradio app and its interface
│   └── config.py             # Configuration (thresholds, file paths, etc.)
│
├── rag/
│   ├── vector_store.py       # Vector store initialization and building
│   ├── retriever.py          # Retriever configuration
│   ├── llm.py                # LLM initialization and prompt management
│   └── embeddings.py         # Embedding functionality for the RAG system uses Ollama
│
├── utils/
│   ├── error_handling.py     # Error handling decorators
│   └── feedback_logger.py    # (Optional) Feedback logging
│
├── data/                     # Iqbal's poetry dataset (already included)
│
├── requirements.txt          # Project dependencies
├── app.py                    # Entry point for the app
└── README.md                 # This file
```

---

## Configuration

Edit `interface/config.py` to set:
- `HUGGING_FACE_TOKEN`: Your personal huggingface token (this can be set up using dotenv. Create a .env file in the home folder and store it as 
HUGGING_FACE_TOKEN = <YOUR_TOKEN>)
- `SCORE_THRESHOLD`: Minimum similarity score for retrieved poems.
- `JSON_FILE_PATH`: Path to your poems data file (already set to the included dataset).

---

## 🚀 Hugging Face Spaces Ready

### In Progress: 
This project is ready to be deployed as a [Hugging Face Space](https://huggingface.co/spaces). The configuration block above (in YAML) tells Hugging Face how to launch the app:
- **sdk**: Uses Gradio for the web interface.
- **app_file**: Entry point for the app (`app.py`).
- **python_version**: Uses Python 3.10.
- **short_description**: Shown in the Space's thumbnail.
- **tags**: For discoverability.

To deploy, simply upload this repository to your Hugging Face account as a new Space.

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements or bug fixes.

---

## License

[MIT License](LICENSE)

---

## Acknowledgements

- Inspired by the poetry of Allama Iqbal.
- Built with Python, Gradio, vector search, and LLM technologies.

---

## References

- [Hugging Face Spaces Configuration Reference](https://huggingface.co/docs/hub/spaces-config-reference)
