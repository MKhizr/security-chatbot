import gradio as gr
from src.week1.rag_chain import build_rag_chain

print("Loading RAG chain...")
chain, vectorstore = build_rag_chain()
print("Ready.")


def answer_question(question: str) -> str:
    if not question.strip():
        return "Please enter a question."
    if not chain:
        return "RAG chain failed to initialize."
    return chain.invoke(question)


demo = gr.Interface(
    fn=answer_question,
    inputs=gr.Textbox(
        label="Ask a security question",
        placeholder="e.g. What does NIST 800-53 say about account management?",
        lines=2
    ),
    outputs=gr.Textbox(
        label="Answer",
        lines=6
    ),
    title="Security Chatbot",
    description="Ask questions about NIST 800-53 security controls. Answers are grounded in the document — no hallucination.",
    examples=[
        ["What does NIST 800-53 say about account management?"],
        ["What are the requirements for remote access?"],
        ["How should organizations handle incident reporting?"],
        ["What is AC-3 about?"],
    ]
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
