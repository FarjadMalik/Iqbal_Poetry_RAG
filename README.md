# Iqbal Poetry RAG System

A Retrieval-Augmented Generation (RAG) system for exploring and querying the poetry of Allama Iqbal. This project leverages vector search and large language models (LLMs) to answer questions about Iqbal's poetry, providing relevant poem excerpts as context.

---

## Features

- **Semantic Search**: Retrieve the most relevant poems for a given question using vector embeddings.
- **LLM-Powered Answers**: Generate answers using a language model, grounded in retrieved poem context.
- **Configurable**: Easily adjust retrieval thresholds, model settings, and data sources.
- **Error Handling**: Robust error management for smoother user experience.
- **(Optional) Feedback Logging**: Log user feedback for continuous improvement.

---

## Installation

### Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) (a fast Python package installer, drop-in replacement for pip)

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

1. **Prepare your data**: Place your poems JSON file at the path specified in `app/config.py` (`JSON_FILE_PATH`).
2. **Run the main application** (example, adjust as needed):

```bash
python app/main.py
```

3. **Query the system**: Enter your question about Iqbal's poetry and receive contextually grounded answers.

---

## Project Structure

```bash
iqbal_poetry_rag/
│
├── app/
│ ├── RAGSystem.py # Main RAG system class
│ ├── main.py # Entry point for the application
│ └── config.py # Configuration (thresholds, file paths, etc.)
│
├── rag/
│ ├── vector_store.py # Vector store initialization and building
│ ├── retriever.py # Retriever configuration
│ ├── llm.py # LLM initialization and prompt management
│
├── utils/
│ ├── error_handling.py # Error handling decorators
│ └── feedback_logger.py # (Optional) Feedback logging
│
├── requirements.txt # Project dependencies
└── README.md # This file
```

---

## Configuration

Edit `app/config.py` to set:

- `SCORE_THRESHOLD`: Minimum similarity score for retrieved poems.
- `JSON_FILE_PATH`: Path to your poems data file.

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements or bug fixes.

---

## License

[MIT License](LICENSE)

---

## Acknowledgements

- Inspired by the poetry of Allama Iqbal.
- Built with Python, vector search, and LLM technologies.