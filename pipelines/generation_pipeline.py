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
    print("🟢Generation PL : Starting to create response")
    """
    Full generation pipeline: chunks → prompt → LLM → answer.

    Returns
    -------
    {
        "answer"  : str        — the model's answer,
        "sources" : List[Dict] — the chunks used to build the prompt.
    }
    """
    prompt, sources = build_prompt(query=query, chunks=retrieved_chunks)

    est_tokens = len(prompt) // 4
    logger.info("[Generation] Prompt sent to LLM — estimated tokens: %d", est_tokens)

    answer = generate_answer(prompt)

    return {
        "answer":  answer,
        "sources": sources,
    }