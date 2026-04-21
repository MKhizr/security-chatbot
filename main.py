from src.week1.api_client import call_ollama
from src.week1.embeddings import build_index, semantic_search

SYSTEM_PROMPT = (
    "You are a cybersecurity expert. "
    "Give concise, technical answers."
)

API_PROMPTS = [
    "What is lateral movement in cybersecurity?",
    "Explain credential dumping as used by attackers.",
    "What is the difference between blue team and red team in cybersecurity?",
]

SEARCH_QUERIES = [
    "lateral movement using stolen credentials",
    "attacker dumps password hashes from memory",
    "command and control over encrypted channel",
]

def run_api_calls():
    print("\n" + "="*60)
    print("API CALLS")
    print("="*60)
    for prompt in API_PROMPTS:
        print(f"\nPrompt: {prompt}")
        resp = call_ollama(prompt, SYSTEM_PROMPT)
        if resp:
            print(f"  [{resp.provider}] {resp.input_tokens}+{resp.output_tokens} tokens")
            print(f"  {resp.content}")

def run_semantic_search(collection, model):
    print("\n" + "="*60)
    print("SEMANTIC SEARCH — MITRE ATT&CK")
    print("="*60)
    for query in SEARCH_QUERIES:
        print(f"\nQuery: '{query}'")
        hits = semantic_search(query, collection, model, top_k=3)
        for hit in hits:
            print(f"  {hit['id']:10} {hit['name']:45} sim={hit['similarity']}")

if __name__ == "__main__":
    run_api_calls()
    collection, model = build_index()
    run_semantic_search(collection, model)
