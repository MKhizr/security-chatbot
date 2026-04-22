from dotenv import load_dotenv
load_dotenv()

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


with gr.Blocks(title="Security Chatbot") as demo:

    gr.Markdown(
        """
        # Security Chatbot
        **RAG-powered** · Grounded in NIST 800-53 · No hallucination · Runs on Llama 3.1
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            question_box = gr.Textbox(
                placeholder="Ask a question about NIST 800-53...",
                label="Your Question",
                lines=3
            )
            submit_btn = gr.Button("Ask", variant="primary")
            gr.Examples(
                examples=[
                    "What does NIST 800-53 say about account management?",
                    "What are the requirements for remote access?",
                    "How should organizations handle incident reporting?",
                    "What is AC-3 about?",
                    "What does IR-4 cover?",
                ],
                inputs=question_box,
                label="Examples"
            )

        with gr.Column(scale=1):
            answer_box = gr.Textbox(
                label="Answer",
                lines=10,
                interactive=False
            )

    gr.Markdown("Built with LangChain · ChromaDB · Groq · Evaluated with BLEU 0.57 / ROUGE 0.50")

    submit_btn.click(
        fn=answer_question,
        inputs=question_box,
        outputs=answer_box
    )
    question_box.submit(
        fn=answer_question,
        inputs=question_box,
        outputs=answer_box
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
