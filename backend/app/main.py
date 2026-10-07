from fastapi import FastAPI, UploadFile, File, HTTPException
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
FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)

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


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "RAG PDF Chatbot API is running!"
    }


# Health check
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# PDF upload endpoint
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

    # Extract text from PDF
    documents = extract_documents_from_pdf(str(file_path))

    # Check if PDF contains readable text
    if not documents:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from this PDF. Please upload a text-based PDF."
        )

    # Split document into chunks
    chunks = split_documents(documents)

    # Check if chunks were created
    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="No readable text was found in the PDF."
        )

    # Create and save FAISS vector store
    vector_store = create_vector_store(chunks)
    save_vector_store(vector_store)

    return {
        "filename": file.filename,
        "message": "PDF uploaded successfully",
        "number_of_pages": len(documents),
        "number_of_chunks": len(chunks)
    }


# Chat request model
class ChatRequest(BaseModel):
    question: str


# Chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):

    result = generate_answer(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }