from __future__ import annotations

from typing import List, Dict, Tuple

_CHARS_PER_CHUNK = 4_000


def _format_chunk(chunk: Dict, max_chars: int = _CHARS_PER_CHUNK) -> str:
    text = chunk["text"][:max_chars]
    page = chunk.get("page", "?")
    cid  = chunk.get("chunk_id", "?")
    return f"[Page {page} | chunk {cid}]\n{text}"


def build_prompt(
    query: str,
    chunks: List[Dict],
    max_chars_per_chunk: int = _CHARS_PER_CHUNK,
) -> Tuple[str, List[Dict]]:
    """
    Assemble a RAG prompt from the query and retrieved chunks.

    Returns
    -------
    (prompt_string, source_list)
        source_list is the list of chunks actually included so the
        caller can attach them to the final response for citation.
    """
    if not chunks:
        raise ValueError("build_prompt received an empty chunk list.")

    formatted = [_format_chunk(c, max_chars_per_chunk) for c in chunks]
    context = "\n\n---\n\n".join(formatted)

    prompt = f"""You are OctoVector, a precise document-QA assistant.
Answer ONLY using the context below. Do not invent facts.
If the answer is not in the context, reply exactly:
"I don't know based on the provided document."

=== CONTEXT START ===
{context}
=== CONTEXT END ===

Question: {query}

Instructions:
- Be concise and factual.
- If you quote a passage, cite the page number in parentheses, e.g. (Page 3).
- Do not repeat the question.

Answer:"""

    return prompt, chunks