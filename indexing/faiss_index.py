from __future__ import annotations

import os
import logging
from typing import Tuple

import faiss
import numpy as np

logger = logging.getLogger(__name__)


class FAISSIndex:
    """
    Thin wrapper around a FAISS flat index.
    Uses inner-product (cosine) similarity — assumes unit vectors.
    """

    def __init__(self, dim: int) -> None:
        self.dim = dim
        self.index: faiss.IndexFlatIP = faiss.IndexFlatIP(dim)
        logger.info("[FAISS] Initialised IndexFlatIP with dim=%d", dim)

    def add(self, embeddings: np.ndarray) -> None:
        """Add a batch of normalised float32 vectors."""
        if embeddings.ndim != 2 or embeddings.shape[1] != self.dim:
            raise ValueError(
                f"Expected shape (n, {self.dim}), got {embeddings.shape}"
            )
        self.index.add(embeddings.astype(np.float32))
        logger.debug("[FAISS] Added %d vectors; total=%d", len(embeddings), self.index.ntotal)


    def search(
        self, query_vector: np.ndarray, k: int = 5
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Return (scores, indices) for the top-k nearest neighbours.
        Higher score = more similar (inner product).
        """
        if self.index.ntotal == 0:
            raise RuntimeError("FAISS index is empty — call add() first.")

        k = min(k, self.index.ntotal) 

        if query_vector.ndim == 1:
            query_vector = query_vector[np.newaxis, :]

        scores, indices = self.index.search(
            query_vector.astype(np.float32), k
        )
        return scores[0], indices[0]

    def save(self, path: str) -> None:
        """Serialise the index to *path* (e.g. "index.faiss")."""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        faiss.write_index(self.index, path)
        logger.info("[FAISS] Index saved → %s", path)

    @classmethod
    def load(cls, path: str, dim: int) -> "FAISSIndex":
        """Deserialise an index previously saved with save()."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"FAISS index file not found: {path}")
        obj = cls.__new__(cls)
        obj.dim = dim
        obj.index = faiss.read_index(path)
        logger.info("[FAISS] Index loaded ← %s (%d vectors)", path, obj.index.ntotal)
        return obj