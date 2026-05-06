import re
from typing import List, Dict


def split_into_sentences(text: str) -> List[str]:
    # Simple sentence splitter
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_text(text: str, chunk_size: int = 250, overlap: int = 50) -> List[str]:
    """
    Sentence-aware chunking with overlap
    chunk_size and overlap are approximate token counts (we approximate via words)
    """

    sentences = split_into_sentences(text)

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        words = sentence.split()
        length = len(words)

        # If adding this sentence exceeds chunk size → finalize chunk
        if current_length + length > chunk_size:
            chunks.append(" ".join(current_chunk))

            # Add overlap
            overlap_words = " ".join(current_chunk).split()[-overlap:]
            current_chunk = [" ".join(overlap_words)]

            current_length = len(overlap_words)

        current_chunk.append(sentence)
        current_length += length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks