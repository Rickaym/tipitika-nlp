import chromadb
from sentence_transformers import CrossEncoder
from typing import Any
import numpy as np

chroma_client = chromadb.PersistentClient(path="../db")
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def process(query: str, model: str) -> Any:
    match model:
        case "abhidhamma-search":
            return query_collection(query, collection_name="abhidhamma-search", n_results=10, cross_encoder_reranking=True)
        case "abhidamma-rag":
            return None
        case _:
            raise Exception(f"Unsupported model {model}")


def query_collection(query: str, collection_name: str, n_results: int, cross_encoder_reranking: bool):
    results = chroma_client.get_collection(collection_name).query(
        query_texts=[query], n_results=n_results
    )
    retrieved_documents = results["documents"][0]
    if cross_encoder_reranking:
        pairs = [[query, doc] for doc in retrieved_documents]
        scores = cross_encoder.predict(pairs)
        order = np.argsort(scores)[::-1]
        print(order)
        retrieved_documents = [retrieved_documents[i] for i in order]
    return zip(results["metadatas"][0], retrieved_documents)  # type: ignore
