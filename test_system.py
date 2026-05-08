from __future__ import annotations

import logging
import sys
import time
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)

from pipelines.ingestion_pipeline import process_pdf
from embedding.embedder import embed_chunks
from pipelines.retrieval_pipeline import retrieve_chunks
from pipelines.generation_pipeline import generate_response


def banner(title: str) -> None:
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def main() -> None:

    pdf_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.getenv("OCTOVECTOR_PDF", "data/raw_pdfs/rag_knowledge_base.pdf")
    )

    # Ingestion 
    banner("STEP 1 — PDF INGESTION")
    t0 = time.time()
    chunks = process_pdf(pdf_path)
    print(f"  Chunks created : {len(chunks)}")
    print(f"  Time           : {time.time() - t0:.2f}s")

    if not chunks:
        print("[ERROR] No chunks extracted. Check the PDF path and content.")
        sys.exit(1)

    # Embedding 
    banner("STEP 2 — EMBEDDING")
    t0 = time.time()
    embeddings = embed_chunks(chunks)
    print(f"  Embedding shape: {embeddings.shape}")
    print(f"  Time           : {time.time() - t0:.2f}s")

    # Query 
    banner("STEP 3 — QUERY INPUT")
    try:
        query = input("\n  Enter your question:\n  > ").strip()
    except KeyboardInterrupt:
        print("\n  Aborted.")
        sys.exit(0)

    if not query:
        print("[ERROR] Empty query.")
        sys.exit(1)

    # Retrieval 
    banner("STEP 4 — RETRIEVAL + RERANKING")
    t0 = time.time()
    retrieved = retrieve_chunks(
        query=query,
        chunks=chunks,
        embeddings=embeddings,
        top_k=5,
    )
    print(f"  Time: {time.time() - t0:.2f}s")

    print(f"\n  TOP {len(retrieved)} RETRIEVED CHUNKS")
    print("  " + "-" * 56)
    for i, chunk in enumerate(retrieved, 1):
        print(f"\n  Rank {i} | Page {chunk.get('page')} | chunk {chunk.get('chunk_id')}")
        if "rrf_score"    in chunk: print(f"  RRF Score    : {chunk['rrf_score']:.4f}")
        if "rerank_score" in chunk: print(f"  Rerank Score : {chunk['rerank_score']:.4f}")
        print(f"  Text preview : {chunk['text'][:300]}…")

    # Generation
    banner("STEP 5 — GENERATION")
    t0 = time.time()

    result = generate_response(query=query, retrieved_chunks=retrieved)
    answer  = result["answer"]
    sources = result["sources"]

    print(f"  Time: {time.time() - t0:.2f}s")

    banner("FINAL ANSWER")
    print(f"\n{answer}")

    print(f"\n  Sources used: {[c.get('chunk_id') for c in sources]}")
    banner("PIPELINE COMPLETE")


if __name__ == "__main__":
    main()