import faiss
import numpy as np


class FAISSIndex:
    def __init__(self, dim: int):
        """
        Initialize FAISS index
        Using L2 (Euclidean distance) for simplicity
        """
        self.index = faiss.IndexFlatL2(dim)

    def add(self, embeddings: np.ndarray):
        """
        Add embeddings to index
        """
        self.index.add(embeddings)

    def search(self, query_vector: np.ndarray, k: int = 5):
        """
        Search top-k similar vectors
        """
        if query_vector.ndim == 1:
            query_vector = np.expand_dims(query_vector, axis=0)

        distances, indices = self.index.search(query_vector, k)

        return distances[0], indices[0]