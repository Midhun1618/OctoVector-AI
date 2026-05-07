from __future__ import annotations

from typing import List, Dict

from utils.config import RRF_K


def reciprocal_rank_fusion(
    dense_results: List[Dict],
    sparse_results: List[Dict],
    k: int = RRF_K,
) -> List[Dict]:
    """
    Merge and re-rank *dense_results* and *sparse_results* using
    Reciprocal Rank Fusion (RRF).

    Each input item must have a "chunk_id" key.

    Returns a list of chunk dicts sorted by descending rrf_score.
    """
    scores: dict[str, float] = {}

    def _accumulate(results: List[Dict]) -> None:
        for rank, item in enumerate(results):
            cid = item["chunk_id"]
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank + 1)

    _accumulate(dense_results)
    _accumulate(sparse_results)

    all_chunks: dict[str, Dict] = {}
    for item in sparse_results:
        all_chunks[item["chunk_id"]] = item
    for item in dense_results:          
        all_chunks[item["chunk_id"]] = item

    max_score = 1.0 / (k + 1) * 2

    ranked = sorted(
        all_chunks.values(),
        key=lambda x: scores[x["chunk_id"]],
        reverse=True,
    )

    for item in ranked:
        raw = scores[item["chunk_id"]]
        item["rrf_score"] = raw / max_score

    return ranked