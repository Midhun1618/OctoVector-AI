from embedding.embedder import embed_query
from indexing.index_manager import IndexManager


class DenseRetriever:
    def __init__(self, index_manager: IndexManager):
        self.index_manager = index_manager

    def retrieve(self, query: str, k: int = 5):
        query_vec = embed_query(query)
        return self.index_manager.search(query_vec, k=k)