
Two production-grade AI engineering projects built with a cybersecurity domain focus.

---

## Security RAG Chatbot

A RAG-powered chatbot that answers natural language questions about NIST 800-53 security controls.

**Evaluation:** BLEU 0.57 · ROUGE 0.50 · tracked across multiple runs in MLflow

**Stack:** Python 3.11 · LangChain · ChromaDB · sentence-transformers · Groq (Llama 3.1 8B) · FastAPI · Gradio · MLflow · Docker

Live demo: https://khizrsec-security-chatbot.hf.space

### Run locally

```bash
git clone https://github.com/MKhizr/security-chatbot.git
cd security-chatbot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # add your GROQ_API_KEY
python -m src.week1.gradio_app
```
Open http://127.0.0.1:7860

---

## Threat Intel Triage Agent

An autonomous AI agent that investigates indicators of compromise — IP addresses, file hashes, and URLs. The agent decides which tools to call, queries VirusTotal, Shodan, and MITRE ATT&CK automatically, then synthesizes findings into a structured JSON threat report.

**Stack:** Python 3.11 · LangGraph · Groq (Llama 3.3 70B) · VirusTotal API · Shodan API · MITRE ATT&CK · Gradio · Pydantic

Live demo: https://khizrsec-threat-intel-agent.hf.space

### Run locally

```bash
cp .env.example .env        # add GROQ_API_KEY, VIRUSTOTAL_API_KEY, SHODAN_API_KEY
python -m src.week2.gradio_app
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
  "malicious_detections": 16,
  "total_engines": 94,
  "country": "Germany",
  "isp": "Stiftung Erneuerbare Freiheit",
  "open_ports": [80],
  "mitre_techniques": [
    {"id": "T1190", "name": "Exploit Public-Facing Application", "tactic": "initial-access"}
  ],
  "summary": "Tor exit node flagged by 16 out of 94 vendors. High risk of C2 activity.",
  "recommendations": ["Block at perimeter firewall", "Investigate internal hosts that contacted this IP"]
}
```

---

## Author

Muhammad Khizr Shahid  
[LinkedIn](https://linkedin.com/in/khizr-shahid) · [GitHub](https://github.com/MKhizr)
