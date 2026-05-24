from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Dict, List

import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


API_URL = "http://127.0.0.1:8000/query"

DATASET_PATH = "test_data.json"

SIMILARITY_THRESHOLD = 0.70

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

print("\n🟢 Loading evaluation embedding model...\n")

embedder = SentenceTransformer(EMBED_MODEL)

def clean_text(text: str) -> str:

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        "",
        text
    )

    return text.strip()


def keyword_score(
    generated: str,
    keywords: List[str],
) -> float:

    if not keywords:
        return 0.0

    generated = clean_text(generated)

    matched = 0

    for kw in keywords:

        if clean_text(kw) in generated:
            matched += 1

    return matched / len(keywords)


def semantic_similarity(
    text1: str,
    text2: str,
) -> float:

    emb1 = embedder.encode([text1])

    emb2 = embedder.encode([text2])

    score = cosine_similarity(
        emb1,
        emb2
    )[0][0]

    return float(score)


def ask_rag(
    question: str,
) -> str:

    response = requests.post(
        API_URL,
        json={
            "question": question
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    # change this if your API response differs
    return data.get(
        "answer",
        ""
    )


# ============================================================
# LOAD DATASET
# ============================================================

dataset_path = Path(DATASET_PATH)

if not dataset_path.exists():

    raise FileNotFoundError(
        f"Dataset not found: {DATASET_PATH}"
    )

with open(
    dataset_path,
    "r",
    encoding="utf-8"
) as f:

    dataset = json.load(f)


# ============================================================
# METRICS STORAGE
# ============================================================

total_questions = len(dataset)

passed_similarity = 0

passed_keywords = 0

all_similarity_scores = []

all_keyword_scores = []

results = []


# ============================================================
# START EVALUATION
# ============================================================

print("=" * 60)
print("🚀 STARTING RAG EVALUATION")
print("=" * 60)

start_time = time.time()

for idx, item in enumerate(dataset, start=1):

    question = item["question"]

    expected = item["expected_answer"]

    keywords = item.get(
        "relevant_keywords",
        []
    )

    difficulty = item.get(
        "difficulty",
        "unknown"
    )

    qtype = item.get(
        "type",
        "unknown"
    )

    print(f"\n[{idx}/{total_questions}]")
    print("-" * 60)

    print(f"Question: {question}")

    # ========================================================
    # GET RAG ANSWER
    # ========================================================

    try:

        generated = ask_rag(question)

    except Exception as e:

        print(f"❌ API ERROR: {e}")

        continue

    print(f"\nGenerated:\n{generated}")

    # ========================================================
    # METRICS
    # ========================================================

    similarity = semantic_similarity(
        expected,
        generated
    )

    keyword_match = keyword_score(
        generated,
        keywords
    )

    similarity_pass = (
        similarity >= SIMILARITY_THRESHOLD
    )

    keyword_pass = (
        keyword_match >= 0.50
    )

    if similarity_pass:
        passed_similarity += 1

    if keyword_pass:
        passed_keywords += 1

    all_similarity_scores.append(similarity)

    all_keyword_scores.append(keyword_match)

    # ========================================================
    # PRINT SCORES
    # ========================================================

    print("\n📊 METRICS")

    print(
        f"Semantic Similarity : "
        f"{similarity:.3f}"
    )

    print(
        f"Keyword Match       : "
        f"{keyword_match:.3f}"
    )

    print(
        f"Similarity Pass     : "
        f"{'✅' if similarity_pass else '❌'}"
    )

    print(
        f"Keyword Pass        : "
        f"{'✅' if keyword_pass else '❌'}"
    )

    results.append(
        {
            "question": question,
            "expected": expected,
            "generated": generated,
            "similarity": similarity,
            "keyword_match": keyword_match,
            "difficulty": difficulty,
            "type": qtype,
        }
    )


# ============================================================
# FINAL REPORT
# ============================================================

total_time = time.time() - start_time

avg_similarity = (
    sum(all_similarity_scores)
    / len(all_similarity_scores)
)

avg_keyword = (
    sum(all_keyword_scores)
    / len(all_keyword_scores)
)

similarity_accuracy = (
    passed_similarity
    / total_questions
) * 100

keyword_accuracy = (
    passed_keywords
    / total_questions
) * 100

overall_score = (
    (
        similarity_accuracy
        + keyword_accuracy
    ) / 2
)

print("\n")
print("=" * 60)
print("📈 FINAL EVALUATION REPORT")
print("=" * 60)

print(
    f"Total Questions        : "
    f"{total_questions}"
)

print(
    f"Average Similarity     : "
    f"{avg_similarity:.3f}"
)

print(
    f"Average Keyword Match  : "
    f"{avg_keyword:.3f}"
)

print(
    f"Similarity Accuracy    : "
    f"{similarity_accuracy:.2f}%"
)

print(
    f"Keyword Accuracy       : "
    f"{keyword_accuracy:.2f}%"
)

print(
    f"\n🏆 OVERALL RAG SCORE    : "
    f"{overall_score:.2f}/100"
)

print(
    f"⏱ Evaluation Time      : "
    f"{total_time:.2f} sec"
)

print("=" * 60)


# ============================================================
# SAVE REPORT
# ============================================================

report = {
    "summary": {
        "total_questions": total_questions,
        "average_similarity": avg_similarity,
        "average_keyword_match": avg_keyword,
        "similarity_accuracy": similarity_accuracy,
        "keyword_accuracy": keyword_accuracy,
        "overall_score": overall_score,
        "evaluation_time_sec": total_time,
    },
    "results": results,
}

with open(
    "evaluation_report.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        report,
        f,
        indent=2,
        ensure_ascii=False
    )

print("\n✅ Saved report to evaluation_report.json")