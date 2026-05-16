from __future__ import annotations

import logging
import re
from typing import Dict, List, Optional

from sentence_transformers import CrossEncoder

from utils.config import RERANK_MODEL, RERANK_TOP_K, RERANK_THRESHOLD
from retrieval.query_analyzer import analyze_query

logger = logging.getLogger(__name__)


class CrossEncoderReranker:
    """Singleton-cached cross-encoder reranker."""

    _model: Optional[CrossEncoder] = None

    def __init__(self) -> None:
        if CrossEncoderReranker._model is None:
            logger.info("[Reranker] Loading model: %s", RERANK_MODEL)
            CrossEncoderReranker._model = CrossEncoder(RERANK_MODEL)
        self.model = CrossEncoderReranker._model

    def rerank(
        self,
        query: str,
        chunks: List[Dict],
        top_k: int = RERANK_TOP_K,
    ) -> List[Dict]:
        """
        Score and rerank chunks for query, return top-k above threshold.
        Always returns at least 1 chunk even if all scores are below threshold.
        """
        if not chunks:
            return []

        logger.info("[Reranker] Scoring %d candidates", len(chunks))

        pairs  = [(query, chunk["text"]) for chunk in chunks]
        scores = self.model.predict(
            pairs,
            show_progress_bar=False,
            convert_to_numpy=True,
        )

        try:
            query_info = analyze_query(query)
            query_len  = max(query_info.get("query_length", 1), 1)
            numbers    = query_info.get("numbers", [])
            keywords   = query_info.get("keywords", [])
        except Exception:
            logger.warning("[Reranker] analyze_query failed, skipping boost")
            query_len, numbers, keywords = 1, [], []

        for chunk, score in zip(chunks, scores):
            text  = chunk["text"].lower()
            boost = 0.0

            for number in numbers:
                if re.search(rf"\b{re.escape(number)}\b", text):
                    boost += 0.1 

            keyword_matches  = sum(1 for w in keywords if w in text)
            boost           += (keyword_matches * 0.02) / query_len

            chunk["rerank_score"] = float(score) + boost

        ranked   = sorted(chunks, key=lambda x: x["rerank_score"], reverse=True)
        top      = ranked[:top_k]

        filtered = [c for c in top if c["rerank_score"] >= RERANK_THRESHOLD]
        result   = filtered if filtered else top[:1]

        logger.info(
            "[Reranker] Returning %d/%d chunks (threshold=%.1f)",
            len(result), len(top), RERANK_THRESHOLD,
        )
        return result