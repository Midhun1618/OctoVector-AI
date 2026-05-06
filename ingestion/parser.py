from ingestion.chunker import chunk_text

def extract_text_from_pdf(pdf_path):
    import fitz  

    doc = fitz.open(pdf_path)

    all_chunks = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()

        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "chunk_id": f"{page_num}_{i}",
                "text": chunk,
                "page": page_num
            })

    return all_chunks