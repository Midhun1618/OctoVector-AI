# ============================================================
# OctoVector AI — Cross-Encoder Reranker
# ============================================================
# Changes:
#  1. Model loaded as lazy singleton (same pattern as embedder)
#     to avoid reloading on every pipeline invocation.
#  2. CORRECTNESS FIX: analyze_query was imported and called but
#     its result was never actually improving ranking in a sound
#     way — raw keyword-count boosts can easily overpower the
#     cross-encoder signal for long queries. Boost is now scaled
#     by query length so short precise queries aren't penalised.
#  3. Numeric boost is now checked with word-boundary regex
#     (r"\b42\b") to avoid "142" matching a query for "42".
#  4. Batch prediction (cross_encoder.predict on all pairs at
#     once) replaces the implicit loop — already the case, but
#     now explicit with show_progress_bar for large corpora.
#  5. Empty chunk list handled gracefully.
#  6. Type hints added.

from __future__ import annotations

import re
import logging
from typing import List, Dict, Optional

from sentence_transformers import CrossEncoder

from utils.config import RERANK_MODEL, RERANK_TOP_K
from retrieval.query_analyzer import analyze_query

logger = logging.getLogger(__name__)

_model: Optional[CrossEncoder] = None


def _get_model() -> CrossEncoder:
    global _model
    if _model is None:
        logger.info("[Reranker] Loading model: %s", RERANK_MODEL)
        _model = CrossEncoder(RERANK_MODEL)
    return _model


class CrossEncoderReranker:

    def __init__(self) -> None:
        # Trigger lazy load at construction time (warms up before first query)
        self.model = _get_model()

    def rerank(
        self,
        query: str,
        chunks: List[Dict],
        top_k: int = RERANK_TOP_K,
    ) -> List[Dict]:
        """
        Score and rerank *chunks* for *query*, return top-k.

        Parameters
        ----------
        query  : User query string.
        chunks : Candidate chunks (each must have a "text" key).
        top_k  : Number of chunks to return.

        Returns
        -------
        List of chunk dicts sorted by descending rerank_score,
        length ≤ top_k.
        """
        if not chunks:
            return []

        pairs = [(query, chunk["text"]) for chunk in chunks]

        scores = self.model.predict(
            pairs,
            show_progress_bar=False,
            convert_to_numpy=True,
        )

        query_info = analyze_query(query)
        query_len  = max(query_info["query_length"], 1)

        for chunk, score in zip(chunks, scores):
            text  = chunk["text"].lower()
            boost = 0.0

            # ── Numeric boost ─────────────────────────────
            # CHANGE: word-boundary match avoids "142" matching "42"
            for number in query_info["numbers"]:
                if re.search(rf"\b{re.escape(number)}\b", text):
                    boost += 0.5

            # ── Keyword boost (length-normalised) ─────────
            # CHANGE: divide by query_len so a 20-keyword query
            # can't drown out the cross-encoder signal.
            keyword_matches = sum(
                1 for word in query_info["keywords"] if word in text
            )
            boost += (keyword_matches * 0.05) / query_len

            chunk["rerank_score"] = float(score) + boost

        ranked = sorted(chunks, key=lambda x: x["rerank_score"], reverse=True)
        return ranked[:top_k]