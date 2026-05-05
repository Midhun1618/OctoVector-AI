from typing import List, Dict

def chunk_text(
    text: str,
    page_num: int,
    chunk_size: int = 150,
    overlap: int = 30
) -> List[Dict]:
    """
    Create overlapping chunks
    """

    words = text.split()
    chunks = []

    start = 0
    chunk_id = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]

        chunk_str = " ".join(chunk_words)

        chunks.append({
            "chunk_id": f"{page_num}_{chunk_id}",
            "text": chunk_str,
            "page": page_num
        })

        start += chunk_size - overlap
        chunk_id += 1

    return chunks