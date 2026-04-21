from src.week1.api_client import call_ollama
from src.week1.embeddings import build_index, semantic_search
from src.week1.rag_chain import build_rag_chain

SYSTEM_PROMPT = (
    "You are a cybersecurity expert. "
    "Give concise, technical answers."
)

API_PROMPTS = [
    "What is lateral movement in cybersecurity?",
    "Explain credential dumping as used by attackers.",
    "What is the difference between a red team and a blue team?",
]

SEARCH_QUERIES = [
    "lateral movement using stolen credentials",
    "attacker dumps password hashes from memory",
]

RAG_QUESTIONS = [
    "What does NIST 800-53 say about account management?",
    "How should organizations handle incident reporting?",
    "What are the requirements for remote access?",
    "What does NIST 800-53 say about cryptography?",
    "What is the difference between a red team and a blue team?",	
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
            print(f"  {resp.content[:200]}")


def run_semantic_search(collection, model):
    print("\n" + "="*60)
    print("SEMANTIC SEARCH — MITRE ATT&CK")
    print("="*60)
    for query in SEARCH_QUERIES:
        print(f"\nQuery: '{query}'")
        hits = semantic_search(query, collection, model, top_k=3)
        for hit in hits:
            print(f"  {hit['id']:10} {hit['name']:45} sim={hit['similarity']}")


def run_rag(chain):
    print("\n" + "="*60)
    print("RAG CHAIN — NIST 800-53")
    print("="*60)
    for question in RAG_QUESTIONS:
        print(f"\nQuestion: {question}")
        answer = chain.invoke(question)
        print(f"Answer: {answer[:300]}")


if __name__ == "__main__":
    run_api_calls()
    collection, model = build_index()
    run_semantic_search(collection, model)
    chain, _ = build_rag_chain()
    if chain:
        run_rag(chain)
