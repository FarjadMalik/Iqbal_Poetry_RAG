#!/usr/bin/env bash
# install Ollama
curl -sSfL https://ollama.ai/install.sh | sh

# optionally pull a model
ollama pull llama3

# then start your app
python app.py
