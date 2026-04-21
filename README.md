# Security Chatbot

Semantic search over MITRE ATT&CK techniques using sentence embeddings,
plus LLM-powered answers to cybersecurity questions running fully locally.

## What it does
- Runs Llama 3.2 locally via Ollama — no API costs, no rate limits
- Embeds 200 MITRE ATT&CK technique descriptions using sentence-transformers
- Stores embeddings in ChromaDB (local vector database)
- Returns top matching techniques for any natural language security query

## Stack
Python 3.9 · Ollama (Llama 3.2) · sentence-transformers · ChromaDB

## Run it
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ollama serve  # in a separate terminal tab
ollama pull llama3.2
python main.py
```
