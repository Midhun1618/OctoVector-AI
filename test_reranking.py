from pipelines.ingestion_pipeline import process_pdf
from embedding.embedder import embed_chunks
from indexing.index_manager import IndexManager
from retrieval.hybrid_retrieval import HybridRetriever
from reranking.cross_encoder import CrossEncoderReranker

print("STARTING TEST")

chunks = process_pdf("sample.pdf")
print("pdf added")

embeddings = embed_chunks(chunks)
print("embedding done")

index_manager = IndexManager()
index_manager.build_index(chunks, embeddings)
print("indexing done")

retriever = HybridRetriever(index_manager, chunks)

query = "What AI projects has the candidate built?"

initial_results = retriever.retrieve(query, k=5)

print("\nBefore Reranking:\n")
for r in initial_results:
    print(f"RRF Score: {r['rrf_score']}")
    print(f"Text: {r['text'][:120]}...\n")

reranker = CrossEncoderReranker()
final_results = reranker.rerank(query, initial_results, top_k=3)

print("\nAfter Reranking:\n")
for r in final_results:
    print(f"Rerank Score: {r['rerank_score']}")
    print(f"Text: {r['text'][:120]}...\n")