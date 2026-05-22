from __future__ import annotations

from typing import List, Dict

from utils.config import RRF_K


def reciprocal_rank_fusion(
    dense_results: List[Dict],
    sparse_results: List[Dict],
    k: int = RRF_K,
) -> List[Dict]:
    print("🟢RRF : Merging and Reranking Dense & Sparse result")

    scores: dict[str, float] = {}

    # Keep strongest candidates only
    dense_results = dense_results[:10]
    sparse_results = sparse_results[:10]

    def _accumulate(
        results: List[Dict],
        source_weight: float,
    ) -> None:

        for rank, item in enumerate(results):

            cid = item["chunk_id"]

            rrf_score = source_weight * (
                1.0 / (k + rank + 1)
            )

            scores[cid] = (
                scores.get(cid, 0.0)
                + rrf_score
            )

    # Dense semantic retrieval gets slightly more importance
    _accumulate(
        dense_results,
        source_weight=1.2
    )

    # Sparse exact keyword matching
    _accumulate(
        sparse_results,
        source_weight=1.0
    )

    all_chunks: dict[str, Dict] = {}

    for item in dense_results + sparse_results:
        all_chunks[item["chunk_id"]] = item

    ranked = sorted(
        all_chunks.values(),
        key=lambda x: scores.get(
            x["chunk_id"],
            0.0
        ),
        reverse=True,
    )

    for item in ranked:
        item["rrf_score"] = scores.get(
            item["chunk_id"],
            0.0
        )

    print("\n===== RRF RESULTS =====")

    for i, item in enumerate(ranked[:15]):

        print(f"\nRank {i+1}")
        print(
            "RRF Score:",
            round(item["rrf_score"],4)
        )

        print(
            item["text"][:250]
        )

    return ranked