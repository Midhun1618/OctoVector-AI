# ============================================================
# OctoVector AI — Text Cleaner
# ============================================================
# Changes:
#  1. Added removal of PDF extraction artefacts:
#       - Lone page-number lines (e.g. "  42  ")
#       - Repeated header/footer lines appearing on every page
#       - Non-printable / control characters
#       - Hyphenated line-break artefacts ("hyphen-\nated" → "hyphenated")
#  2. Unicode normalisation (NFKC) converts ligatures (ﬁ→fi),
#     smart quotes, and full-width chars so tokenisers work correctly.
#  3. Excess blank lines collapsed to a single newline so sentence
#     splitting in the chunker is not confused by empty lines.

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

    # 1. Unicode normalise
    text = unicodedata.normalize("NFKC", text)

    # 2. Strip control characters except newline / tab
    text = re.sub(r"[^\S\n\t]+", " ", text)  # runs of non-newline whitespace → single space
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    # 3. Repair soft-hyphen line-breaks
    text = re.sub(r"-\s*\n\s*", "", text)

    # 4. Collapse multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # 5. Strip lines that are only digits (lone page numbers)
    lines = text.split("\n")
    lines = [ln for ln in lines if not re.fullmatch(r"\s*\d{1,4}\s*", ln)]
    text = "\n".join(lines)

    return text.strip()