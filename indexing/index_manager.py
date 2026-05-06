import numpy as np
from indexing.faiss_index import FAISSIndex


class IndexManager:
    def __init__(self):
        self.index = None
        self.chunks = []

    def build_index(self, chunks, embeddings: np.ndarray):
        """
        Create FAISS index and store chunks
        """
        dim = embeddings.shape[1]

        self.index = FAISSIndex(dim)
        self.index.add(embeddings)

        self.chunks = chunks

    def search(self, query_vector: np.ndarray, k: int = 5):
        """
        Search and return matching chunks
        """
        distances, indices = self.index.search(query_vector, k)

        results = []
        for idx, dist in zip(indices, distances):
            if idx < len(self.chunks):
                chunk = self.chunks[idx]
                chunk_copy = chunk.copy()
                chunk_copy["score"] = float(dist)
                results.append(chunk_copy)

        return results