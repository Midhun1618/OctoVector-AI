from ingestion.parser import extract_text_from_pdf


def process_pdf(pdf_path):
    print("🟢Ingestion PL : Processing initialized ")
    """
    End-to-end ingestion:
    PDF → cleaned → chunked
    """

    chunks = extract_text_from_pdf(pdf_path)

    return chunks