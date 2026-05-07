# ============================================================
# OctoVector AI — Retrieval Pipeline
# ============================================================
# Changes:
#  1. BUG FIX: CrossEncoderReranker was instantiated at module
#     import time (top-level). If the reranker model isn't
#     available on import, the whole module crashes even for
#     unrelated use. Moved to lazy instantiation inside function.
#  2. IndexManager is now created once per retrieve_chunks call
#     and can optionally receive a pre-built manager for
#     persistent use (avoids rebuilding the index on every call
#     in a server / interactive scenario).
#  3. top_k is capped at len(chunks) to avoid a FAISS crash
#     when fewer chunks exist than requested.
#  4. Logging added at each stage with timing info.

from __future__ import annotations

import logging
import time
from typing import List, Dict, Optional

import numpy as np

from indexing.index_manager import IndexManager
from retrieval.hybrid_retrieval import HybridRetriever
from reranking.cross_encoder import CrossEncoderReranker
from utils.config import FINAL_TOP_K

logger = logging.getLogger(__name__)

# Lazy singletons — initialised on first call
_reranker: Optional[CrossEncoderReranker] = None


def _get_reranker() -> CrossEncoderReranker:
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoderReranker()
    return _reranker


def retrieve_chunks(
    query: str,
    chunks: List[Dict],
    embeddings: np.ndarray,
    top_k: int = FINAL_TOP_K,
    index_manager: Optional[IndexManager] = None,
) -> List[Dict]:
    """
    Full retrieval pipeline: embeddings → hybrid retrieval → reranking.

    Parameters
    ----------
    query         : User question.
    chunks        : All parsed chunks (must align with embeddings rows).
    embeddings    : Pre-computed chunk embeddings, shape (n, dim).
    top_k         : Final number of chunks to return.
    index_manager : Pass a pre-built IndexManager to skip rebuilding.

    Returns
    -------
    List of top-k chunk dicts enriched with retrieval scores.
    """
    if not chunks:
        raise ValueError("retrieve_chunks received empty chunk list.")

    # CHANGE: cap top_k to avoid requesting more chunks than exist
    top_k = min(top_k, len(chunks))

    # ── Build index (or reuse) ────────────────────────────────
    t0 = time.time()
    if index_manager is None:
        index_manager = IndexManager()
        index_manager.build_index(chunks=chunks, embeddings=embeddings)
    logger.info("[Retrieval] Index ready in %.2fs", time.time() - t0)

    # ── Hybrid retrieval ──────────────────────────────────────
    t0 = time.time()
    hybrid_retriever = HybridRetriever(
        index_manager=index_manager,
        chunks=chunks,
    )
    candidate_k = min(20, len(chunks))
    retrieved = hybrid_retriever.retrieve(query=query, k=candidate_k)
    logger.info("[Retrieval] Hybrid retrieved %d candidates in %.2fs", len(retrieved), time.time() - t0)

    # ── Reranking ─────────────────────────────────────────────
    t0 = time.time()
    reranker = _get_reranker()
    reranked = reranker.rerank(query=query, chunks=retrieved, top_k=top_k)
    logger.info("[Retrieval] Reranked to %d chunks in %.2fs", len(reranked), time.time() - t0)

    return reranked