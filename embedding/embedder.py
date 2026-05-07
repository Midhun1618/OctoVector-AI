from sentence_transformers import SentenceTransformer
from typing import List, Dict
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks: List[Dict]) -> np.ndarray:
    """
    Convert chunk texts into embeddings
    """
    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    return embeddings


def embed_query(query: str) -> np.ndarray:
    """
    Convert query into embedding
    """
    return model.encode(query, convert_to_numpy=True)