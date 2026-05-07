# ============================================================
# OctoVector AI — PDF Parser
# ============================================================
# Changes:
#  1. BUG FIX: cleaner.clean_text() was imported but never
#     called. Text now goes through cleaning before chunking.
#  2. Pages with no extractable text (scanned images) are
#     logged and skipped rather than producing empty chunks.
#  3. extract_text_from_pdf now accepts an optional page_range
#     so large documents can be processed in sections.
#  4. chunk_id is now a proper string key:
#     f"p{page_num}_c{i}" — avoids confusion with
#     integer arithmetic on "1_0" strings.
#  5. Added page metadata: char_count is stored so downstream
#     modules can filter trivially-short pages.

from __future__ import annotations

import logging
from typing import List, Dict, Optional, Tuple

from ingestion.chunker import chunk_text
from ingestion.cleaner import clean_text

logger = logging.getLogger(__name__)


def extract_text_from_pdf(
    pdf_path: str,
    page_range: Optional[Tuple[int, int]] = None,
) -> List[Dict]:
    """
    Parse *pdf_path* and return a list of chunk dicts.

    Each dict has:
        chunk_id  : str  — unique identifier "p{page}_c{index}"
        text      : str  — cleaned chunk text
        page      : int  — 1-based page number
        char_count: int  — character count of the chunk

    Parameters
    ----------
    pdf_path   : Path to the PDF file.
    page_range : Optional (start, end) 1-based inclusive page numbers.
                 E.g. (1, 10) processes pages 1–10 only.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError as exc:
        raise ImportError(
            "PyMuPDF is required: pip install pymupdf"
        ) from exc

    doc = fitz.open(pdf_path)
    total_pages = doc.page_count

    # Determine page range
    start_page = 1
    end_page   = total_pages
    if page_range:
        start_page = max(1, page_range[0])
        end_page   = min(total_pages, page_range[1])

    logger.info(
        "[Parser] Processing '%s' pages %d–%d of %d",
        pdf_path, start_page, end_page, total_pages,
    )

    all_chunks: List[Dict] = []

    for page_num in range(start_page, end_page + 1):
        page = doc[page_num - 1]  # fitz is 0-based
        raw_text = page.get_text()

        if not raw_text.strip():
            logger.warning("[Parser] Page %d has no extractable text — skipping.", page_num)
            continue

        # CHANGE: clean before chunking
        cleaned_text = clean_text(raw_text)

        if not cleaned_text:
            logger.warning("[Parser] Page %d empty after cleaning — skipping.", page_num)
            continue

        chunks = chunk_text(cleaned_text)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "chunk_id":   f"p{page_num}_c{i}",   # CHANGE: clearer ID format
                "text":       chunk,
                "page":       page_num,
                "char_count": len(chunk),
            })

    doc.close()
    logger.info("[Parser] Total chunks produced: %d", len(all_chunks))
    return all_chunks