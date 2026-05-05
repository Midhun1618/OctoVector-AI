from pipelines.ingestion_pipeline import process_pdf

chunks = process_pdf("sample.pdf")

print("Total chunks:", len(chunks))
print("First chunk:", chunks[0])