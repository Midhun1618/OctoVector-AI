from retrieval.dense_retrieval import DenseRetriever
from retrieval.sparse_retrieval import SparseRetriever
from retrieval.rrf import reciprocal_rank_fusion
from utils.config import DENSE_TOP_K, SPARSE_TOP_K


class HybridRetriever:
    def __init__(self, index_manager, chunks):
        self.dense = DenseRetriever(index_manager)
        self.sparse = SparseRetriever(chunks)

    def retrieve(self, query: str, k: int = 20):
        dense_results = self.dense.retrieve(query, k=DENSE_TOP_K)
        sparse_results = self.sparse.retrieve(query, k=SPARSE_TOP_K)

        fused = reciprocal_rank_fusion(dense_results, sparse_results)

        return fused[:k]