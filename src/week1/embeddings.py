import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from src.week1.mitre_loader import load_mitre_techniques

COLLECTION_NAME = "mitre_techniques"
EMBED_MODEL = "all-MiniLM-L6-v2"


def build_index():
    techniques = load_mitre_techniques(max_techniques=200)
    model = SentenceTransformer(EMBED_MODEL)

    client = chromadb.Client()
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    texts = [
        f"{t['name']}: {t['description']}"
        for t in techniques
    ]
    embeddings = model.encode(texts, show_progress_bar=True).tolist()
    ids = [t["id"] for t in techniques]
    metadatas = [
        {"name": t["name"], "tactics": ", ".join(t["tactics"])}
        for t in techniques
    ]

    collection.add(
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Indexed {len(techniques)} techniques into ChromaDB")
    return collection, model


def semantic_search(
    query: str,
    collection,
    model,
    top_k: int = 5
) -> List[Dict]:
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    hits = []
    for i in range(len(results["ids"][0])):
        hits.append({
            "id": results["ids"][0][i],
            "name": results["metadatas"][0][i]["name"],
            "tactics": results["metadatas"][0][i]["tactics"],
            "similarity": round(1 - results["distances"][0][i], 4),
            "snippet": results["documents"][0][i][:200],
        })
    return hits
