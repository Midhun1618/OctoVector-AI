# ============================================================
# OctoVector AI — Generation Pipeline
# ============================================================
# Changes:
#  1. CORRECTNESS FIX: build_prompt now returns (prompt, sources)
#     tuple — this module now unpacks both and returns sources
#     alongside the answer so the caller can display citations.
#  2. Added token-count estimate in the log so you can monitor
#     prompt size without a tokeniser dependency.
#  3. generate_response returns a dict instead of a raw string:
#       {
#           "answer"  : str,
#           "sources" : List[Dict],   # chunks actually used
#       }
#     This breaks the old interface intentionally — it makes the
#     system transparent and testable.

from __future__ import annotations

import logging
from typing import List, Dict

from generation.prompt_builder import build_prompt
from generation.llm_client import generate_answer

logger = logging.getLogger(__name__)


def generate_response(
    query: str,
    retrieved_chunks: List[Dict],
) -> Dict:
    """
    Full generation pipeline: chunks → prompt → LLM → answer.

    Returns
    -------
    {
        "answer"  : str        — the model's answer,
        "sources" : List[Dict] — the chunks used to build the prompt.
    }
    """
    # CHANGE: unpack (prompt, sources) tuple from build_prompt
    prompt, sources = build_prompt(query=query, chunks=retrieved_chunks)

    # Rough token estimate (1 token ≈ 4 chars) — helpful for debugging
    est_tokens = len(prompt) // 4
    logger.info("[Generation] Prompt sent to LLM — estimated tokens: %d", est_tokens)

    answer = generate_answer(prompt)

    return {
        "answer":  answer,
        "sources": sources,
    }