from __future__ import annotations
import json
import time
import sys
from pathlib import Path

# ==========================================================

# PROJECT ROOT

# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# ==========================================================

# IMPORTS

# ==========================================================

from pipelines.ingestion_pipeline import process_pdf
from embedding.embedder import embed_chunks
from pipelines.retrieval_pipeline import retrieve_chunks
from indexing.index_manager import IndexManager

# ==========================================================

# CONFIG

# ==========================================================

PDF_PATH = "../uploads/heavy_content.pdf"
DATASET_FILE = "dataset.json"

TOP_K = 5

# ==========================================================

# LOAD DATASET

# ==========================================================

with open(DATASET_FILE, "r", encoding="utf-8") as f:dataset = json.load(f)

print(f"\n🟢 Loaded {len(dataset)} evaluation samples")

# ==========================================================

# PDF INGESTION

# ==========================================================

print("\n============================================================")
print(" PDF INGESTION ")
print("============================================================")

chunks = process_pdf(PDF_PATH)

print(f"\n🟢 Chunks created: {len(chunks)}")

# ==========================================================

# EMBEDDINGS

# ==========================================================

print("\n============================================================")
print(" EMBEDDING ")
print("============================================================")

embeddings = embed_chunks(chunks)

print(
f"\n🟢 Embedding Shape: "
f"{embeddings.shape}"
)

# ==========================================================

# BUILD INDEX ONCE

# ==========================================================

print("\n============================================================")
print(" BUILDING INDEX ")
print("============================================================")

index_manager = IndexManager()

index_manager.build_index(
chunks=chunks,
embeddings=embeddings
)

print("\n🟢 Index Built Successfully")

# ==========================================================

# METRICS

# ==========================================================

total_questions = len(dataset)

successful_retrievals = 0

total_recall = 0.0

total_time = 0.0

# ==========================================================

# EVALUATION LOOP

# ==========================================================

for idx, sample in enumerate(dataset, start=1):

    question = sample["question"]

    expected_keywords = sample[
        "expected_keywords"
    ]

    print("\n")
    print("=" * 60)
    print(f"QUESTION {idx}")
    print("=" * 60)

    print(f"\nQ: {question}")

    start = time.time()

    retrieved_chunks = retrieve_chunks(
        query=question,
        chunks=chunks,
        embeddings=embeddings,
        top_k=TOP_K,
        index_manager=index_manager
    )

    retrieval_time = (
        time.time() - start
    )

    total_time += retrieval_time

    retrieved_text = " ".join(
        chunk["text"]
        for chunk in retrieved_chunks
    ).lower()

    matched_keywords = []

    for keyword in expected_keywords:

        if keyword.lower() in retrieved_text:

            matched_keywords.append(
                keyword
            )

    recall = (
        len(matched_keywords)
        / len(expected_keywords)
    )

    total_recall += recall

    if len(matched_keywords) > 0:
        successful_retrievals += 1

    print(
        f"\nExpected Keywords : "
        f"{expected_keywords}"
    )

    print(
        f"Matched Keywords  : "
        f"{matched_keywords}"
    )

    print(
        f"Keyword Hits      : "
        f"{len(matched_keywords)}"
        f"/"
        f"{len(expected_keywords)}"
    )

    print(
        f"Recall            : "
        f"{recall:.3f}"
    )

    print(
        f"Retrieval Time    : "
        f"{retrieval_time:.2f}s"
    )

print("\n")
print("=" * 60)
print(f"QUESTION {idx}")
print("=" * 60)

print(f"\nQ: {question}")

start = time.time()

retrieved_chunks = retrieve_chunks(
    query=question,
    chunks=chunks,
    embeddings=embeddings,
    top_k=TOP_K,
    index_manager=index_manager
)

retrieval_time = (
    time.time() - start
)

total_time += retrieval_time

# ======================================================
# MERGE RETRIEVED CHUNKS
# ======================================================

retrieved_text = " ".join(
    chunk["text"]
    for chunk in retrieved_chunks
).lower()

# ======================================================
# KEYWORD MATCHING
# ======================================================

matched_keywords = []

for keyword in expected_keywords:

    if keyword.lower() in retrieved_text:

        matched_keywords.append(
            keyword
        )

# ======================================================
# RECALL
# ======================================================

recall = (
    len(matched_keywords)
    / len(expected_keywords)
)

total_recall += recall

if len(matched_keywords) > 0:
    successful_retrievals += 1

# ======================================================
# OUTPUT
# ======================================================

print(
    f"\nExpected Keywords : "
    f"{expected_keywords}"
)

print(
    f"Matched Keywords  : "
    f"{matched_keywords}"
)

print(
    f"Keyword Hits      : "
    f"{len(matched_keywords)}"
    f"/"
    f"{len(expected_keywords)}"
)

print(
    f"Recall            : "
    f"{recall:.3f}"
)

print(
    f"Retrieval Time    : "
    f"{retrieval_time:.2f}s"
)

# ==========================================================

# FINAL RESULTS

# ==========================================================

print("\n")
print("=" * 60)
print("FINAL RESULTS")
print("=" * 60)

success_rate = (
successful_retrievals
/ total_questions
) * 100

avg_recall = (
total_recall
/ total_questions
)

avg_time = (
total_time
/ total_questions
)
print("\nDEBUG")
print("successful_retrievals =", successful_retrievals)
print("total_recall =", total_recall)
print("total_questions =", total_questions)

print(
f"\nQuestions Tested      : "
f"{total_questions}"
)

print(
f"Retrieval Success Rate: "
f"{success_rate:.2f}%"
)

print(
f"Average Recall        : "
f"{avg_recall:.4f}"
)

print(
f"Average Retrieval Time: "
f"{avg_time:.2f}s"
)

print("\n============================================================")
print("EVALUATION COMPLETE")
print("============================================================")
