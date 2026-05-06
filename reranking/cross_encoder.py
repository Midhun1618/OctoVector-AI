print("CROSS_ENCODER FILE LOADED")
from sentence_transformers import CrossEncoder
from typing import List, Dict

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


class CrossEncoderReranker:
    def __init__(self):
        self.model = model

    def rerank(self, query: str, chunks: List[Dict], top_k: int = 5):
        """
        Rerank retrieved chunks using cross-encoder
        """
        pairs = [(query, chunk["text"]) for chunk in chunks]

        scores = self.model.predict(pairs)

        for chunk, score in zip(chunks, scores):
            chunk["rerank_score"] = float(score)

        ranked = sorted(
            chunks,
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return ranked[:top_k]