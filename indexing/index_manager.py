from __future__ import annotations

import json
import os
import logging
from typing import List, Dict, Optional

import numpy as np

from indexing.faiss_index import FAISSIndex

logger = logging.getLogger(__name__)

_CHUNKS_FILENAME = "chunks.json"
_INDEX_FILENAME  = "faiss.index"


class IndexManager:
    def __init__(self) -> None:
        self.index: Optional[FAISSIndex] = None
        self.chunks: List[Dict] = []


    def build_index(
        self,
        chunks: List[Dict],
        embeddings: np.ndarray,
    ) -> None:
        print("🟢Index Manager : Create FAISS index from embedding & chunks")
        """
        Build a FAISS index from *embeddings* and store *chunks*.

        Raises ValueError if lengths don't match.
        """
        if len(chunks) != embeddings.shape[0]:
            raise ValueError(
                f"Mismatch: {len(chunks)} chunks but {embeddings.shape[0]} embeddings."
            )

        dim = embeddings.shape[1]
        self.index = FAISSIndex(dim)
        self.index.add(embeddings)
        self.chunks = chunks
        logger.info("[IndexManager] Built index: %d vectors, dim=%d", len(chunks), dim)


    def search(
        self,
        query_vector: np.ndarray,
        k: int = 5,
    ) -> List[Dict]:
        print("🟢Index Manager : Searching index upto K")
        """
        Search the index and return up to *k* matching chunk dicts,
        each annotated with a 'score' key (higher = more similar).
        """
        if self.index is None:
            raise RuntimeError("Index not built. Call build_index() first.")

        scores, indices = self.index.search(query_vector, k)

        results: List[Dict] = []
        for idx, score in zip(indices, scores):
            if idx == -1 or idx >= len(self.chunks):
                continue
            chunk_copy = self.chunks[idx].copy()
            chunk_copy["score"] = float(score)
            results.append(chunk_copy)

        return results

    def save(self, directory: str) -> None:
        print("🟢Index Manager : saving index & chunk")
        """Persist index and chunks to *directory*."""
        os.makedirs(directory, exist_ok=True)

        # Save FAISS index
        self.index.save(os.path.join(directory, _INDEX_FILENAME))

        # Save chunks as JSON
        chunks_path = os.path.join(directory, _CHUNKS_FILENAME)
        with open(chunks_path, "w", encoding="utf-8") as fh:
            json.dump(self.chunks, fh, ensure_ascii=False)

        logger.info("[IndexManager] Saved to %s", directory)

    def load(self, directory: str, dim: int) -> None:
        print("🟢Index Manager : Loading chunks & index")
        """Load index and chunks previously saved with save()."""
        index_path  = os.path.join(directory, _INDEX_FILENAME)
        chunks_path = os.path.join(directory, _CHUNKS_FILENAME)

        self.index = FAISSIndex.load(index_path, dim)

        with open(chunks_path, "r", encoding="utf-8") as fh:
            self.chunks = json.load(fh)

        logger.info(
            "[IndexManager] Loaded %d chunks from %s", len(self.chunks), directory
        )