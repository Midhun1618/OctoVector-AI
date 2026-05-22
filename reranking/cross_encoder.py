from __future__ import annotations

import logging
import re
from typing import Dict, List, Optional

from sentence_transformers import CrossEncoder

from utils.config import (
    RERANK_MODEL,
    RERANK_TOP_K,
    RERANK_THRESHOLD
)

from retrieval.query_analyzer import analyze_query

logger = logging.getLogger(__name__)


class CrossEncoderReranker:
    """Singleton cached cross encoder reranker"""

    _model: Optional[CrossEncoder] = None

    def __init__(self):

        if CrossEncoderReranker._model is None:
            logger.info(
                "[Reranker] Loading model: %s",
                RERANK_MODEL
            )

            CrossEncoderReranker._model = CrossEncoder(
                RERANK_MODEL
            )

        self.model = CrossEncoderReranker._model

    def rerank(
        self,
        query: str,
        chunks: List[Dict],
        top_k: int = RERANK_TOP_K,
    ) -> List[Dict]:

        if not chunks:
            return []

        logger.info(
            "[Reranker] Scoring %d candidates",
            len(chunks)
        )

        pairs = [
            (query, chunk["text"])
            for chunk in chunks
        ]

        scores = self.model.predict(
            pairs,
            show_progress_bar=False,
            convert_to_numpy=True
        )

        try:

            query_info = analyze_query(query)

            query_len = max(
                query_info.get(
                    "query_length",
                    1
                ),
                1
            )

            numbers = query_info.get(
                "numbers",
                []
            )

            keywords = query_info.get(
                "keywords",
                []
            )

        except Exception:

            logger.warning(
                "[Reranker] analyze_query failed"
            )

            query_len = 1
            numbers = []
            keywords = []

        for chunk,score in zip(chunks,scores):

            text = chunk["text"].lower()

            boost = 0.0

            for number in numbers:

                if re.search(
                    rf"\b{re.escape(number)}\b",
                    text
                ):
                    boost += 0.1

            keyword_matches = sum(
                1
                for w in keywords
                if re.search(
                    rf"\b{re.escape(w)}\b",
                    text
                )
            )

            boost += (
                keyword_matches * 0.02
            ) / query_len

            chunk["rerank_score"] = (
                float(score)
                + boost
            )

        ranked = sorted(
            chunks,
            key=lambda x:x["rerank_score"],
            reverse=True
        )

        print("\n===== CROSS ENCODER SCORES =====")

        for i,item in enumerate(ranked[:10]):

            print(
                f"\nRank {i+1}"
            )

            print(
                "Score:",
                round(
                    item["rerank_score"],
                    3
                )
            )

            print(
                item["text"][:300]
            )

        top = ranked[:top_k]

        filtered = [

            c
            for c in top
            if c["rerank_score"] >= RERANK_THRESHOLD

        ]

        if len(filtered) == 0:

            filtered = top[:2]

        result = filtered

        logger.info(
            "[Reranker] Returning %d/%d chunks (threshold=%.2f)",
            len(result),
            len(top),
            RERANK_THRESHOLD
        )

        return result