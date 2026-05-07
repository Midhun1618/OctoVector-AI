from __future__ import annotations

import re
import logging
from typing import List

from utils.config import CHUNK_SIZE, CHUNK_OVERLAP

logger = logging.getLogger(__name__)

_ABBREV_PATTERN = re.compile(
    r"\b(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|Fig|No|Vol|vs|etc|approx|e\.g|i\.e)\.",
    re.IGNORECASE,
)

_MIN_CHUNK_WORDS = 10


def split_into_sentences(text: str) -> List[str]:
    """
    Split *text* into sentences using punctuation boundaries,
    while respecting common abbreviations.
    """
    masked = _ABBREV_PATTERN.sub(lambda m: m.group().replace(".", "<!DOT!>"), text)

    parts = re.split(r"(?<=[.!?])\s+", masked)

    sentences = [
        p.replace("<!DOT!>", ".").strip()
        for p in parts
        if p.strip()
    ]
    return sentences


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> List[str]:
    """
    Sentence-aware chunking with word-count-based overlap.

    Parameters
    ----------
    text       : Raw page / document text.
    chunk_size : Target size in words.
    overlap    : Number of words carried forward from the previous chunk.

    Returns
    -------
    List of non-empty chunk strings.
    """
    text = text.strip()
    if not text:
        return []

    sentences = split_into_sentences(text)

    chunks: List[str] = []
    current_words: List[str] = []

    for sentence in sentences:
        s_words = sentence.split()

        if len(current_words) + len(s_words) > chunk_size and current_words:
            chunk_str = " ".join(current_words)

            if len(current_words) >= _MIN_CHUNK_WORDS:
                chunks.append(chunk_str)

            current_words = current_words[-overlap:] if overlap else []

        current_words.extend(s_words)

    if current_words:
        chunk_str = " ".join(current_words)
        if len(current_words) >= _MIN_CHUNK_WORDS:
            chunks.append(chunk_str)
        elif chunks:
            chunks[-1] = chunks[-1] + " " + chunk_str

    logger.debug("[Chunker] Produced %d chunks from %d sentences", len(chunks), len(sentences))
    return chunks