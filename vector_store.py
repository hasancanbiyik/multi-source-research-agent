# vector_store.py
import chromadb
from chromadb.utils import embedding_functions

# I'll use OpenAI embeddings
openai_embedder = embedding_functions.OpenAIEmbeddingFunction(
    api_key=None,              # it will pick up OPENAI_API_KEY from env
    model_name="text-embedding-3-small"
)

# Initialize Chroma and get/create a collection
def init_vector_db():
    client = chromadb.Client()
    collection = client.get_or_create_collection(
        name="research_docs",
        embedding_function=openai_embedder,
    )
    return collection

def add_texts(collection, texts: list[str], metadatas: list[dict]):
    """
    Store texts + metadata (like source URL) into the vector DB.
    ids must be unique strings.
    """
    ids = [f"doc_{i}" for i in range(len(texts))]
    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids,
    )

def query(collection, query_text: str, k: int = 3):
    """
    Retrieve top-k most similar docs to the query.
    Returns list of {text, metadata, distance}
    """
    results = collection.query(
        query_texts=[query_text],
        n_results=k,
    )
    # Chroma returns dict with 'documents', 'metadatas', 'distances'
    hits = []
    for i in range(len(results["documents"][0])):
        hits.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })
    return hits
