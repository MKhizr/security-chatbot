# Security Chatbot

A RAG-powered security chatbot that answers questions about NIST 800-53 
controls using local LLMs. 

## What it does
- Answers natural language questions grounded in NIST 800-53 documents
- Uses Llama 3.2 locally via Ollama — no API costs, fully offline capable
- Retrieves relevant document chunks using ChromaDB vector database
- Evaluated with BLEU and ROUGE scores tracked in MLflow
- REST API via FastAPI with API key authentication
- Web UI via Gradio

## Stack
Python 3.11 · LangChain · ChromaDB · sentence-transformers · 
Ollama (Llama 3.2) · FastAPI · Gradio · MLflow · Docker

## Run the web UI
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ollama serve  # terminal tab 1
ollama pull llama3.2
python -m src.week1.gradio_app  # terminal tab 2
```
Open http://127.0.0.1:7860

## Run the API
```bash
uvicorn src.week1.api:app --reload
curl -X POST http://127.0.0.1:8000/ask \
  -H "x-api-key: dev-key" \
  -H "Content-Type: application/json" \
  -d '{"question": "What does NIST 800-53 say about account management?"}'
```

## Run evaluation
```bash
python -m src.week1.evaluate
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5001
```
Open http://127.0.0.1:5001
