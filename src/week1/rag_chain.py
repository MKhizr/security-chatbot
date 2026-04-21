from langchain_ollama import OllamaLLM
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import DirectoryLoader, TextLoader
import os

EMBED_MODEL = "all-MiniLM-L6-v2"
OLLAMA_MODEL = "llama3.2"


def load_documents():
    """Load documents from the data directory."""
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created {data_dir}/ folder — add your .txt documents there")
        return []

    loader = DirectoryLoader(
        data_dir,
        glob="**/*.txt",
        loader_cls=TextLoader
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} documents")
    return docs


def build_rag_chain():
    """Build and return the full RAG chain."""
    docs = load_documents()

    if not docs:
        print("No documents found — add .txt files to the data/ folder")
        return None, None

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks")

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="security_docs"
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_template("""
You are a cybersecurity expert. Answer the question using only the context below.
If the answer is not in the context, say "I don't have enough information on that."

Context:
{context}

Question:
{question}

Answer:""")

    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    llm = OllamaLLM(model=OLLAMA_MODEL, base_url=ollama_host)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, vectorstore

def build_index_only():
    """Build just the vectorstore without the full chain - for evaluation."""
    docs = load_documents()
    if not docs:
        return None

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="security_docs_eval"
    )
    return vectorstore
