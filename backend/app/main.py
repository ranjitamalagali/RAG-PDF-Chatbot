from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
import os
from app.pdf_processor import extract_documents_from_pdf
from app.rag import split_documents, generate_answer
from app.embeddings import create_vector_store, save_vector_store


# Load environment variables
load_dotenv()


app = FastAPI(
    title="RAG PDF Chatbot API",
    description="Backend API for a RAG-based PDF chatbot",
    version="1.0.0"
)


# CORS configuration
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PDF upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "RAG PDF Chatbot API is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are allowed"
        }

    file_path = UPLOAD_DIR / file.filename

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    # Extract PDF pages with metadata
    documents = extract_documents_from_pdf(str(file_path))

    # Split documents into chunks
    chunks = split_documents(documents)

    # Create FAISS vector store
    vector_store = create_vector_store(chunks)

    # Save FAISS vector store
    save_vector_store(vector_store)

    return {
        "filename": file.filename,
        "message": "PDF uploaded successfully",
        "number_of_pages": len(documents),
        "number_of_chunks": len(chunks)
    }


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
async def chat(request: ChatRequest):

    result = generate_answer(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }