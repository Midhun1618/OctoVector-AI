from __future__ import annotations

import re
import unicodedata


def clean_text(text: str) -> str:
    """
    Clean raw PDF-extracted text.

    Steps
    -----
    1. Unicode normalisation (NFKC)
    2. Remove control characters (keep \\n and \\t)
    3. Fix hyphenated line-breaks ("hyphen-\\nated" → "hyphenated")
    4. Collapse multiple blank lines to one
    5. Normalise whitespace within lines
    6. Strip lone page-number lines (a line that is only digits)
    7. Final strip
    """
    if not text:
        return ""

    text = unicodedata.normalize("NFKC", text)

    text = re.sub(r"[^\S\n\t]+", " ", text) 
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    text = re.sub(r"-\s*\n\s*", "", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    lines = text.split("\n")
    lines = [ln for ln in lines if not re.fullmatch(r"\s*\d{1,4}\s*", ln)]
    text = "\n".join(lines)

    return text.strip()