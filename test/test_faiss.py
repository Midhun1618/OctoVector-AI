from pipelines.ingestion_pipeline import process_pdf
from embedding.embedder import embed_chunks, embed_query
from indexing.index_manager import IndexManager

chunks = process_pdf("sample.pdf")

embeddings = embed_chunks(chunks)

index_manager = IndexManager()
index_manager.build_index(chunks, embeddings)

query = "What is the candidate's experience?"
query_vec = embed_query(query)

results = index_manager.search(query_vec, k=3)

print("\nTop Results:")
for r in results:
    print(f"\nScore: {r['score']}")
    print(f"Page: {r['page']}")
    print(f"Text: {r['text'][:200]}...")