from pipelines.ingestion_pipeline import process_pdf
from embedding.embedder import embed_chunks

chunks = process_pdf("sample.pdf")

embeddings = embed_chunks(chunks)

print("Chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)