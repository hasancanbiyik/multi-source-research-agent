import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set in environment variables.")

openai_embedder = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_KEY,
    model_name="text-embedding-3-small"
)

def init_vector_db():
    client = chromadb.Client()
    collection = client.get_or_create_collection(
        name="research_docs",
        embedding_function=openai_embedder,
    )
    return collection

def add_texts(collection, texts: list[str], metadatas: list[dict]):
    ids = [f"doc_{i}" for i in range(len(texts))]
    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids,
    )

def query(collection, query_text: str, k: int = 3):
    results = collection.query(
        query_texts=[query_text],
        n_results=k,
    )
    hits = []
    for i in range(len(results["documents"][0])):
        hits.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })
    return hits
