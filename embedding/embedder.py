from __future__ import annotations

import numpy as np
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer

from utils.config import EMBEDDING_MODEL

_model: Optional[SentenceTransformer] = None


def _get_model() -> SentenceTransformer:
    """
    Lazy singleton — loads the model only on first call.
    """
    global _model
    if _model is None:
        print(f"[Embedder] Loading model: {EMBEDDING_MODEL}")
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def embed_chunks(
    chunks: List[Dict],
    batch_size: int = 64,
    normalize: bool = True,
) -> np.ndarray:
    print("🟢Embedder : Chunks to Float32")
    """
    Convert a list of chunk dicts into a float32 embedding matrix.

    Parameters
    ----------
    chunks     : list of dicts, each must contain a "text" key.
    batch_size : number of texts encoded per forward pass.
    normalize  : if True, L2-normalise every vector (recommended).

    Returns
    -------
    np.ndarray of shape (len(chunks), embedding_dim), dtype float32.
    """
    if not chunks:
        raise ValueError("embed_chunks received an empty chunk list.")

    model = _get_model()
    texts = [chunk["text"] for chunk in chunks]

    embeddings: np.ndarray = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=normalize,
    )

    return embeddings.astype(np.float32)


def embed_query(query: str, normalize: bool = True) -> np.ndarray:
    print("🟢Embedder : Query Embedding")
    """
    Convert a query string into a 1-D embedding vector.

    Parameters
    ----------
    query     : the user's question string.
    normalize : if True, L2-normalise the vector (recommended).

    Returns
    -------
    np.ndarray of shape (embedding_dim,), dtype float32.
    """
    if not query.strip():
        raise ValueError("embed_query received an empty query string.")

    model = _get_model()
    vec: np.ndarray = model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=normalize,
    )
    return vec.astype(np.float32)