import fitz  # PyMuPDF
from typing import List, Tuple

def extract_text_from_pdf(file_path: str) -> List[Tuple[int, str]]:
    """
    Extract text from PDF page by page.

    Returns:
        List of (page_number, text)
    """
    doc = fitz.open(file_path)
    pages = []

    for i, page in enumerate(doc):
        text = page.get_text("text")
        pages.append((i + 1, text))

    return pages