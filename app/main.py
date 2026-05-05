from pipelines.ingestion_pipeline import process_pdf

chunks = process_pdf("sample.pdf")

print(len(chunks))
print(chunks[0])