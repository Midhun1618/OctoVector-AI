from __future__ import annotations

import json
import time
import requests
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ============================================================
# CONFIG
# ============================================================

API_URL = "http://127.0.0.1:8000/query"

DATASET_PATH = "test_dataset.json"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ============================================================
# LOAD MODEL
# ============================================================

print("🟢 Loading evaluation embedding model...")

embedder = SentenceTransformer(
    EMBED_MODEL
)

# ============================================================
# LOAD DATASET
# ============================================================

with open(
    DATASET_PATH,
    "r",
    encoding="utf-8"
) as f:

    dataset = json.load(f)

print(
    f"🟢 Loaded {len(dataset)} evaluation samples"
)

# ============================================================
# METRICS STORAGE
# ============================================================

semantic_scores = []
exact_matches = []
response_times = []
length_ratios = []

successful_queries = 0

# ============================================================
# EVALUATION LOOP
# ============================================================

for idx, sample in enumerate(
    dataset,
    start=1
):

    question = sample["question"]
    expected = sample["expected_answer"]

    print("\n")
    print("=" * 60)
    print(f"QUESTION {idx}")
    print("=" * 60)

    print(f"\nQ: {question}")

    start_time = time.time()

    try:

        response = requests.post(
            API_URL,
            json={
                "question": question
            },
            timeout=120
        )

        elapsed = (
            time.time() - start_time
        )

        response_times.append(
            elapsed
        )

        predicted = response.json().get(
            "answer",
            ""
        )

        successful_queries += 1

    except Exception as e:

        print(
            f"❌ Request Failed: {e}"
        )

        continue

    print("\nEXPECTED:")
    print(expected)

    print("\nPREDICTED:")
    print(predicted)

    # ========================================================
    # EXACT MATCH
    # ========================================================

    em = int(
        expected.strip().lower()
        ==
        predicted.strip().lower()
    )

    exact_matches.append(em)

    # ========================================================
    # SEMANTIC SIMILARITY
    # ========================================================

    expected_emb = embedder.encode(
        expected
    ).reshape(1, -1)

    predicted_emb = embedder.encode(
        predicted
    ).reshape(1, -1)

    similarity = cosine_similarity(
        expected_emb,
        predicted_emb
    )[0][0]

    semantic_scores.append(
        similarity
    )

    # ========================================================
    # LENGTH RATIO
    # ========================================================

    expected_len = max(
        len(expected.split()),
        1
    )

    predicted_len = len(
        predicted.split()
    )

    ratio = (
        predicted_len
        /
        expected_len
    )

    length_ratios.append(
        ratio
    )

    print(
        f"\nSemantic Similarity: "
        f"{similarity:.4f}"
    )

    print(
        f"Exact Match: "
        f"{em}"
    )

    print(
        f"Response Time: "
        f"{elapsed:.2f}s"
    )

# ============================================================
# FINAL REPORT
# ============================================================

print("\n")
print("=" * 70)
print("FINAL EVALUATION REPORT")
print("=" * 70)

total_questions = len(dataset)

success_rate = (
    successful_queries
    /
    total_questions
) * 100

avg_similarity = (
    np.mean(semantic_scores)
    if semantic_scores
    else 0
)

avg_exact_match = (
    np.mean(exact_matches)
    if exact_matches
    else 0
)

avg_response_time = (
    np.mean(response_times)
    if response_times
    else 0
)

avg_length_ratio = (
    np.mean(length_ratios)
    if length_ratios
    else 0
)

print(
    f"\nTotal Questions: "
    f"{total_questions}"
)

print(
    f"Successful Queries: "
    f"{successful_queries}"
)

print(
    f"Success Rate: "
    f"{success_rate:.2f}%"
)

print(
    f"\nAverage Semantic Similarity: "
    f"{avg_similarity:.4f}"
)

print(
    f"Average Exact Match: "
    f"{avg_exact_match:.4f}"
)

print(
    f"Average Response Time: "
    f"{avg_response_time:.2f}s"
)

print(
    f"Average Length Ratio: "
    f"{avg_length_ratio:.2f}"
)

print("\n")

# ============================================================
# INTERPRETATION
# ============================================================

print("INTERPRETATION")

if avg_similarity >= 0.90:
    print("🟢 Excellent semantic quality")
elif avg_similarity >= 0.80:
    print("🟢 Very good semantic quality")
elif avg_similarity >= 0.70:
    print("🟡 Acceptable semantic quality")
else:
    print("🔴 Poor semantic quality")

if avg_response_time <= 2:
    print("🟢 Fast responses")
elif avg_response_time <= 5:
    print("🟡 Moderate responses")
else:
    print("🔴 Slow responses")