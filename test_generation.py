from pipelines.ingestion_pipeline import process_pdf
from embedding.embedder import embed_chunks
from indexing.index_manager import IndexManager
from retrieval.hybrid_retrieval import HybridRetriever
from reranking.cross_encoder import CrossEncoderReranker
from generation.prompt_builder import build_prompt
from generation.llm_client import generate_answer

# 1. Ingest
chunks = process_pdf("sample.pdf")

# 2. Embed
embeddings = embed_chunks(chunks)

# 3. Index
index_manager = IndexManager()
index_manager.build_index(chunks, embeddings)

# 4. Retrieve
retriever = HybridRetriever(index_manager, chunks)
query = "What AI projects has the candidate built?"

retrieved = retriever.retrieve(query, k=5)

# 5. Rerank
reranker = CrossEncoderReranker()
final_chunks = reranker.rerank(query, retrieved, top_k=3)

# 6. Build prompt
prompt = build_prompt(query, final_chunks)

print("\n--- PROMPT ---\n")
print(prompt[:500])

# 7. Generate answer
answer = generate_answer(prompt)

print("\n--- FINAL ANSWER ---\n")
print(answer)