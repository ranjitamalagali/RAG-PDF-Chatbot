from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def create_embeddings():
    return HuggingFaceEmbeddings(
        model_name=MODEL_NAME
    )


def create_vector_store(chunks):
    embeddings = create_embeddings()

    vector_store = FAISS.from_documents(
        chunks,
        embedding=embeddings
    )

    return vector_store


def save_vector_store(vector_store, path="vectorstore"):
    vector_store.save_local(path)