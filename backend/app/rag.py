from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.embeddings import create_embeddings
from langchain_community.vectorstores import FAISS
from google import genai
import os


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


def load_vector_store(path="vectorstore"):
    embeddings = create_embeddings()

    vector_store = FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store


def search_documents(question: str, k=4):
    vector_store = load_vector_store()

    documents = vector_store.similarity_search(
        question,
        k=k
    )

    return documents


def generate_answer(question: str):
    documents = search_documents(question)

    context_parts = []
    sources = []

    for document in documents:
        page = document.metadata.get("page", "Unknown")

        context_parts.append(
            f"[Page {page}]\n{document.page_content}"
        )

        if page not in [source["page"] for source in sources]:
            sources.append({
                "page": page
            })

    context = "\n\n".join(context_parts)

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    prompt = f"""
You are a helpful PDF question-answering assistant.

Answer the user's question using ONLY the context provided below.

If the answer cannot be found in the context, say:

"I couldn't find the answer in the uploaded PDF."

Do not make up information.

Do NOT include a Sources section in your answer.
The application will display the sources separately.

Context:

{context}

Question:

{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return {
        "answer": response.text,
        "sources": sources
    }