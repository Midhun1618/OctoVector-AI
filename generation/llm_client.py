from __future__ import annotations
import time
import logging
import os
from typing import Optional
import requests
from utils.config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_BASE_URL

logger = logging.getLogger(__name__)

_RETRYABLE_CODES = {429, 500, 502, 503, 504}
_MAX_RETRIES = 3
_BACKOFF_BASE = 2.0


def _build_url() -> str:
    return f"{GEMINI_BASE_URL}/{GEMINI_MODEL}:generateContent"


def _build_payload(prompt: str) -> dict:
    return {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 1024,
        },
    }



def _parse_response(data: dict) -> str:
    try:
        parts = data["candidates"][0]["content"]["parts"]

        text = "".join(
            part.get("text", "")
            for part in parts
        )

        return text.strip()

    except (KeyError, IndexError) as exc:
        raise RuntimeError(
            f"Unexpected Gemini response shape: {exc}\n{data}"
        ) from exc
    
    
def generate_answer(prompt: str, api_key: Optional[str] = None) -> str:
    print("🟢LLM : Starting to Generate Response")
    """
    Send *prompt* to Gemini and return the generated text.

    Parameters
    ----------
    prompt  : The fully-built prompt string.
    api_key : Override key (useful for tests). Falls back to config.

    Returns
    -------
    The model's answer as a plain string.

    Raises
    ------
    RuntimeError if all retries are exhausted or the response is malformed.
    """
    key = api_key or GEMINI_API_KEY
    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. "
            "Export it as an environment variable before running."
        )

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": key,
    }
    payload = _build_payload(prompt)
    url = _build_url()

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30,
            )
        except requests.exceptions.RequestException as exc:
            logger.warning("[LLM] Network error on attempt %d: %s", attempt, exc)
            if attempt == _MAX_RETRIES:
                raise RuntimeError(f"LLM request failed after {_MAX_RETRIES} attempts: {exc}") from exc
            time.sleep(_BACKOFF_BASE ** attempt)
            continue

        if response.status_code == 200:
            return _parse_response(response.json())

        if response.status_code in _RETRYABLE_CODES and attempt < _MAX_RETRIES:
            wait = _BACKOFF_BASE ** attempt
            logger.warning(
                "[LLM] HTTP %d on attempt %d — retrying in %.1fs",
                response.status_code, attempt, wait,
            )
            time.sleep(wait)
            continue

        raise RuntimeError(
            f"Gemini API returned HTTP {response.status_code}: {response.text}"
        )
    if response.status_code == 200:
        data=response.json()

        print("\n===== RAW GEMINI RESPONSE =====")
        print(data)

        return _parse_response(data)

    raise RuntimeError("LLM request exhausted all retries.")