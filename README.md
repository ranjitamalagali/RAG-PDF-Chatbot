# RAG-Based PDF Chatbot

An AI-powered PDF question-answering application built using Retrieval-Augmented Generation (RAG). Users can upload a PDF and ask questions about its content. The system retrieves relevant document chunks using FAISS and generates grounded answers using Google Gemini.

## Features

- Upload PDF documents
- Extract text using PyPDF2
- Split documents into chunks using LangChain
- Generate embeddings using Hugging Face
- Store and search embeddings using FAISS
- Generate answers using Google Gemini API
- Display source page references
- Interactive React.js chatbot interface
- FastAPI REST API

## Tech Stack

### Backend

- Python
- FastAPI
- LangChain
- PyPDF2
- FAISS
- Hugging Face Embeddings
- Google Gemini API

### Frontend

- React.js
- Vite
- JavaScript
- CSS

### Tools

- Git
- GitHub
- VS Code

## RAG Workflow

```text
PDF Upload
    ↓
PyPDF2 Text Extraction
    ↓
LangChain Text Chunking
    ↓
Hugging Face Embeddings
    ↓
FAISS Vector Store
    ↓
Similarity Search
    ↓
Relevant PDF Chunks
    ↓
Google Gemini
    ↓
AI Answer + Source Pages
    ↓
React.js Interface
