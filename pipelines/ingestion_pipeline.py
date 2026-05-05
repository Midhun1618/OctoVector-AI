import os
from ingestion.parser import extract_text_from_pdf
from ingestion.cleaner import clean_text
from ingestion.chunker import chunk_text

def process_pdf(file_path: str):
    """
    Full ingestion pipeline:
    PDF → clean → chunk
    """

    pages = extract_text_from_pdf(file_path)

    all_chunks = []

    for page_num, text in pages:
        cleaned = clean_text(text)
        chunks = chunk_text(cleaned, page_num)
        all_chunks.extend(chunks)

    return all_chunks