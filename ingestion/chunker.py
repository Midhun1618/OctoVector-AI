from __future__ import annotations

import re
from typing import List


class Chunker:
    def __init__(
        self,
        chunk_size: int = 80,
        overlap: int = 40,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_sentences(
        self,
        text: str,
    ) -> List[str]:

        print("🟢Chunker : spliting sentence")

        text = re.sub(
            r"(Chapter\s+\d+)",
            r" \1",
            text,
            flags=re.IGNORECASE
        )

        sentences = re.split(
            r'(?<=[.!?])\s+',
            text
        )

        cleaned = [
            s.strip()
            for s in sentences
            if len(s.strip()) > 5
        ]

        return cleaned

    def chunk(
        self,
        text: str,
    ) -> List[str]:

        print("🟢Chunker : chunking text")

        sentences = self.split_sentences(text)

        chunks = []
        current_words = []

        for sentence in sentences:

            sentence = sentence.strip()

            if re.search(
                r"^Chapter\s+\d+",
                sentence,
                re.IGNORECASE
            ):

                if current_words:
                    joined = " ".join(current_words)

                    if len(joined.split()) > 5:
                        chunks.append(joined)

                current_words = []

            words = sentence.split()

            if (
                len(current_words)
                + len(words)
                > self.chunk_size
            ):

                joined = " ".join(current_words)

                if len(joined.split()) > 5:
                    chunks.append(joined)

                overlap_words = current_words[
                    -self.overlap:
                ]

                current_words = overlap_words

            current_words.extend(words)

        if current_words:

            joined = " ".join(current_words)

            if len(joined.split()) > 5:
                chunks.append(joined)

        print("\n===== CHUNK DEBUG =====")

        for i, chunk in enumerate(
            chunks[:10],
            start=1
        ):
            print(f"\nChunk {i}")
            print(
                f"Words: {len(chunk.split())}"
            )
            print(chunk[:500])

        return chunks

def chunk_text(
    text: str,
    chunk_size: int = 80,
    overlap: int = 50,
):
    chunker = Chunker(
        chunk_size=chunk_size,
        overlap=overlap
    )

    return chunker.chunk(text)