Two production-grade AI engineering projects built with a cybersecurity domain focus.

---

## Security RAG Chatbot

A RAG-powered chatbot that answers questions about NIST 800-53 security controls.

**Stack:** Python 3.11 · LangChain · ChromaDB · sentence-transformers · Ollama (Llama 3.2) · FastAPI · Gradio · MLflow · Docker

**Evaluation:** BLEU, ROUGE --> tracked in MLflow across multiple runs

### Run it
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ollama serve                        # terminal tab 1
ollama pull llama3.2
python -m src.week1.gradio_app      # terminal tab 2
```
Open http://127.0.0.1:7860

### Run the API
```bash
uvicorn src.week1.api:app --reload
curl -X POST http://127.0.0.1:8000/ask \
  -H "x-api-key: dev-key" \
  -H "Content-Type: application/json" \
  -d '{"question": "What does NIST 800-53 say about account management?"}'
```

### Run evaluation
```bash
python -m src.week1.evaluate
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5001
```
Open http://127.0.0.1:5001

---

## Project 2 — Threat Intel Triage Agent

An autonomous AI agent that investigates indicators of compromise (IOCs) —
IP addresses, file hashes, and URLs — by reasoning over multiple threat
intelligence tools and producing a structured JSON threat report.

**Stack:** Python 3.11 · LangGraph · Ollama (Mistral) · VirusTotal API · Shodan API · MITRE ATT&CK · Gradio · Pydantic

**What it does:** Input one IOC → agent calls VirusTotal + Shodan + MITRE ATT&CK
autonomously → outputs structured JSON with severity, TTPs, CVEs, and recommendations

### Run it
```bash
ollama serve                        # terminal tab 1
ollama pull mistral
python -m src.week2.gradio_app      # terminal tab 2
```
Open http://127.0.0.1:7861

### Example output
Input: `185.220.101.45`
```json
{
  "ioc": "185.220.101.45",
  "ioc_type": "ip",
  "severity": "high",
  "verdict": "malicious",
  "malicious_detections": 7,
  "total_engines": 94,
  "country": "United States",
  "mitre_techniques": [{"id": "T1071", "name": "Application Layer Protocol", "tactic": "Command and Control"}],
  "recommendations": ["Block IP at perimeter firewall", "Investigate internal hosts that communicated with this IP"]
}
```

---

## Setup

```bash
git clone https://github.com/MKhizr/security-chatbot.git
cd security-chatbot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your API keys
ollama serve
ollama pull llama3.2
ollama pull mistral
```

Required API keys:
- VIRUSTOTAL_API_KEY
- SHODAN_API_KEY
- APP_API_KEY

---

## Author
Muhammad Khizr Shahid · [LinkedIn](https://linkedin.com/in/khizr-shahid) ·
