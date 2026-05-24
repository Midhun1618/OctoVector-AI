from __future__ import annotations

import json
import requests
import time
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# CONFIG
# ============================================================

API_URL = "http://127.0.0.1:8000/query"

DATASET_PATH = "dataset.json"

SIMILARITY_THRESHOLD = 0.65

REQUEST_DELAY = 10


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("\n🟢 Loading evaluation embedding model...\n")

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# ============================================================
# LOAD DATASET
# ============================================================

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    dataset = json.load(f)

print(f"🟢 Loaded {len(dataset)} evaluation samples\n")


# ============================================================
# METRICS STORAGE
# ============================================================

total_questions = len(dataset)

correct_answers = 0

faithful_answers = 0

relevant_answers = 0

similarity_scores = []


# ============================================================
# EVALUATION LOOP
# ============================================================

for idx, sample in enumerate(dataset, start=1):

    question = sample["question"]

    expected_answer = sample["expected_answer"]

    print("\n===================================================")

    print(f"QUESTION {idx}")

    print("===================================================\n")

    print(f"Q: {question}\n")

    # --------------------------------------------------------
    # CALL API
    # --------------------------------------------------------

    try:

        response = requests.post(
            API_URL,
            json={
                "question": question
            }
        )

    except Exception as e:

        print(f"❌ Request Failed: {e}")

        continue

    # --------------------------------------------------------
    # CHECK RESPONSE
    # --------------------------------------------------------

    if response.status_code != 200:

        print(
            f"❌ API ERROR: {response.status_code}"
        )

        print(response.text)

        continue

    try:

        result = response.json()

    except Exception:

        print("❌ Invalid JSON response")

        print(response.text)

        continue

    predicted_answer = result.get(
        "answer",
        ""
    )

    print(f"EXPECTED:\n{expected_answer}\n")

    print(f"PREDICTED:\n{predicted_answer}\n")

    # --------------------------------------------------------
    # SEMANTIC SIMILARITY
    # --------------------------------------------------------

    expected_embedding = embedding_model.encode(
        [expected_answer]
    )

    predicted_embedding = embedding_model.encode(
        [predicted_answer]
    )

    similarity = cosine_similarity(
        expected_embedding,
        predicted_embedding
    )[0][0]

    similarity_scores.append(similarity)

    print(f"Semantic Similarity: {similarity:.4f}")

    # --------------------------------------------------------
    # ACCURACY
    # --------------------------------------------------------

    if similarity >= SIMILARITY_THRESHOLD:

        correct_answers += 1

        print("✅ Correct")

    else:

        print("❌ Incorrect")

    # --------------------------------------------------------
    # ANSWER RELEVANCE
    # --------------------------------------------------------

    if similarity >= 0.60:

        relevant_answers += 1

    # --------------------------------------------------------
    # FAITHFULNESS
    # --------------------------------------------------------

    hallucination_phrases = [
        "i think",
        "maybe",
        "probably",
        "might be",
        "possibly"
    ]

    hallucinated = any(
        phrase in predicted_answer.lower()
        for phrase in hallucination_phrases
    )

    if not hallucinated:

        faithful_answers += 1

    # --------------------------------------------------------
    # DELAY
    # --------------------------------------------------------

    time.sleep(REQUEST_DELAY)


# ============================================================
# FINAL METRICS
# ============================================================

accuracy = (
    correct_answers / total_questions
) * 100

avg_similarity = (
    np.mean(similarity_scores)
) * 100

faithfulness = (
    faithful_answers / total_questions
) * 100

answer_relevance = (
    relevant_answers / total_questions
) * 100


# ============================================================
# RESULTS
# ============================================================

print("\n\n===================================================")

print(" FINAL EVALUATION RESULTS ")

print("===================================================\n")

print(f"Total Questions        : {total_questions}")

print(f"Correct Answers        : {correct_answers}")

print(f"Accuracy               : {accuracy:.2f}%")

print(
    f"Average Semantic Score : "
    f"{avg_similarity:.2f}%"
)

print(
    f"Faithfulness Score     : "
    f"{faithfulness:.2f}%"
)

print(
    f"Answer Relevance       : "
    f"{answer_relevance:.2f}%"
)

print("\n===================================================\n")