import mlflow
import os
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import BleuScore, RougeScore
from langchain_huggingface import HuggingFaceEmbeddings
from src.week1.rag_chain import build_rag_chain

questions = [
    "What does NIST 800-53 say about account management?",
    "What are the requirements for remote access?",
    "How should organizations handle incident reporting?",
    "What is AC-3 about?",
    "What does IR-4 cover?",
    "What is the purpose of access control policies?",
    "What must organizations do about system accounts?",
    "What does AC-1 require organizations to do?",
    "What are the incident handling steps?",
    "What must be monitored during remote access sessions?",
]

ground_truths = [
    "Organizations must manage information system accounts including establishing, activating, modifying, reviewing, disabling, and removing accounts.",
    "Organizations must establish usage restrictions and implement guidance for remote access sessions. All remote access sessions must be monitored and controlled.",
    "Organizations must report security incidents to appropriate authorities within defined timeframes.",
    "AC-3 is about access enforcement - the system must enforce approved authorizations for logical access to information and system resources.",
    "IR-4 covers incident handling capability including preparation, detection, analysis, containment, eradication, and recovery.",
    "The purpose is to develop, document, and disseminate access control policies addressing purpose, scope, roles, responsibilities, and compliance.",
    "Organizations must manage accounts including establishing, activating, modifying, reviewing, disabling, and removing accounts.",
    "AC-1 requires organizations to develop, document, and disseminate access control policies and procedures.",
    "Incident handling steps include preparation, detection, analysis, containment, eradication, and recovery.",
    "All remote access sessions must be monitored and controlled.",
]


def run_evaluation():
    print("Building RAG chain...")
    chain, vectorstore = build_rag_chain()

    if not chain:
        print("RAG chain failed to initialize")
        return

    print("Running questions through RAG pipeline...")
    answers = []
    contexts = []

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    for question in questions:
        answer = chain.invoke(question)
        answers.append(answer)
        docs = retriever.invoke(question)
        contexts.append([doc.page_content for doc in docs])
        print(f"  Q: {question[:50]}... done")

    dataset = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    })

    print("\nRunning evaluation with BLEU and ROUGE scores...")
    metrics = [BleuScore(), RougeScore()]
    results = evaluate(dataset, metrics=metrics)

    bleu = results['bleu_score']
    rouge = results['rouge_score(mode=fmeasure)']

    print("\n" + "="*60)
    print("EVALUATION SCORES")
    print("="*60)
    bleu_val = bleu[0] if isinstance(bleu, list) else bleu
    rouge_val = rouge[0] if isinstance(rouge, list) else rouge
    print(f"BLEU Score:   {bleu_val:.4f}")
    print(f"ROUGE Score:  {rouge_val:.4f}")

    print("\nLogging to MLflow...")
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("security-rag-evaluation")
    with mlflow.start_run(run_name="rag-eval-v1"):
        mlflow.log_param("model", "llama3.2")
        mlflow.log_param("chunk_size", 500)
        mlflow.log_param("chunk_overlap", 50)
        mlflow.log_param("retriever_k", 3)
        mlflow.log_param("num_questions", len(questions))
        mlflow.log_metric("bleu_score", bleu_val)
        mlflow.log_metric("rouge_score", rouge_val)

    print("Logged to MLflow successfully")
    return results

if __name__ == "__main__":
    run_evaluation()
