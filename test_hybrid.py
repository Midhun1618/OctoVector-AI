from pipelines.ingestion_pipeline import process_pdf
from embedding.embedder import embed_chunks
from indexing.index_manager import IndexManager
from retrieval.hybrid_retrieval import HybridRetriever

# 1. Ingest
chunks = process_pdf("sample.pdf")

# 2. Embed
embeddings = embed_chunks(chunks)

# 3. Index
index_manager = IndexManager()
index_manager.build_index(chunks, embeddings)

# 4. Hybrid Retriever
retriever = HybridRetriever(index_manager, chunks)

# 5. Query
query = "What AI projects has the candidate built?"

results = retriever.retrieve(query, k=3)

print("\nHybrid Results:\n")

for r in results:
    print(f"Score: {r.get('score', 'N/A')}")
    print(f"Page: {r['page']}")
    print(f"Text: {r['text'][:200]}...")
    print(f"RRF Score: {r['rrf_score']}\n")