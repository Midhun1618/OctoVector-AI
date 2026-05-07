from pipelines.ingestion_pipeline import process_pdf
from embedding.embedder import embed_chunks
from indexing.index_manager import IndexManager
from retrieval.hybrid_retrieval import HybridRetriever


# ------------------------
# CONFIG
# ------------------------
PDF_PATH = "data/raw_pdfs/octovector_rag_testdoc.pdf"

QUERY = "NB-Embed-v2 vs text-embedding-3-large dimension difference 768 3072 embedding size impact"

TOP_K = 30


# ------------------------
# STEP 1: Load + Chunk
# ------------------------
print("\n--- PROCESSING PDF ---")
chunks = process_pdf(PDF_PATH)
print(f"Total chunks: {len(chunks)}")


# ------------------------
# STEP 2: Embeddings
# ------------------------
print("\n--- EMBEDDING ---")
embeddings = embed_chunks(chunks)
print(f"Embedding shape: {embeddings.shape}")


# ------------------------
# STEP 3: Index
# ------------------------
print("\n--- INDEXING ---")
index_manager = IndexManager()
index_manager.build_index(chunks, embeddings)


# ------------------------
# STEP 4: Retrieval
# ------------------------
print("\n--- HYBRID RETRIEVAL ---")
retriever = HybridRetriever(index_manager, chunks)

results = retriever.retrieve(QUERY, k=TOP_K)


# ------------------------
# STEP 5: DEBUG OUTPUT
# ------------------------
print(f"\nTop {TOP_K} Retrieved Chunks:\n")

FOUND = False

for i, chunk in enumerate(results):
    text = chunk["text"]

    print(f"\n--- Rank {i+1} ---")
    print(text[:300])

    # 🔍 Check if answer exists
    if any(keyword in text for keyword in ["768", "3072", "NB-Embed-v2", "text-embedding-3-large"]):
        print("✅ >>> POSSIBLE ANSWER CHUNK FOUND <<<")
        FOUND = True


# ------------------------
# FINAL RESULT
# ------------------------
if not FOUND:
    print("\n❌ ANSWER NOT FOUND IN TOP RESULTS")
else:
    print("\n✅ ANSWER EXISTS IN RETRIEVED SET")