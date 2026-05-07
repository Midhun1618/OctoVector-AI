from rank_bm25 import BM25Okapi


class SparseRetriever:
    def __init__(self, chunks):
        """
        Initialize BM25 with chunk texts
        """
        self.chunks = chunks
        self.corpus = [chunk["text"].split() for chunk in chunks]
        self.bm25 = BM25Okapi(self.corpus)

    def retrieve(self, query: str, k: int = 5):
        print("🟢Sparse R : Filtering Top K chunks with BM25")
        """
        Return top-k chunks based on BM25
        """
        tokenized_query = query.split()
        scores = self.bm25.get_scores(tokenized_query)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:k]

        results = []
        for idx in ranked_indices:
            chunk = self.chunks[idx].copy()
            chunk["score"] = float(scores[idx])
            results.append(chunk)

        return results