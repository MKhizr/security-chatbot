from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from src.week1.rag_chain import build_rag_chain

load_dotenv()

app = FastAPI(title="Security Chatbot API")

chain, vectorstore = build_rag_chain()


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    question: str
    answer: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=QuestionResponse)
def ask(
    request: QuestionRequest,
    x_api_key: Optional[str] = Header(None)
):
    if x_api_key != os.getenv("APP_API_KEY", "dev-key"):
        raise HTTPException(status_code=401, detail="Invalid API key")

    if not chain:
        raise HTTPException(status_code=503, detail="RAG chain not initialized")

    answer = chain.invoke(request.question)
    return QuestionResponse(question=request.question, answer=answer)
