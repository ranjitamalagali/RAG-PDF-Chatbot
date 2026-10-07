from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS
from google import genai
import os


class GeminiEmbeddings(Embeddings):

    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def embed_documents(self, texts):
        result = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=texts
        )

        return [embedding.values for embedding in result.embeddings]

    def embed_query(self, text):
        result = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )

        return result.embeddings[0].values


def create_embeddings():
    return GeminiEmbeddings()


def create_vector_store(chunks):
    embeddings = create_embeddings()

    vector_store = FAISS.from_documents(
        chunks,
        embedding=embeddings
    )

    return vector_store


def save_vector_store(vector_store, path="vectorstore"):
    vector_store.save_local(path)