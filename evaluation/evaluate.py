from __future__ import annotations

import json
import time
import requests

DATASET_FILE = "test_dataset.json"

API_URL = "http://127.0.0.1:8000/query"

with open(DATASET_FILE, "r", encoding="utf-8") as f:
    dataset = json.load(f)

print(f"\n🟢 Loaded {len(dataset)} evaluation samples")

total_questions = len(dataset)

successful_retrievals = 0

total_precision = 0.0
total_recall = 0.0

total_time = 0.0

for idx, sample in enumerate(dataset, start=1):

    question = sample["question"]
    expected_keywords = sample["expected_keywords"]

    print("\n" + "=" * 60)
    print(f"QUESTION {idx}")
    print("=" * 60)

    print(f"\nQ: {question}")

    start = time.time()

    response = requests.post(
        API_URL,
        json={"question": question},
        timeout=120
    )

    end = time.time()

    query_time = end - start
    total_time += query_time

    predicted_answer = response.json()["answer"]

    print("\nANSWER:")
    print(predicted_answer)

    answer_lower = predicted_answer.lower()

    matched_keywords = []

    for keyword in expected_keywords:

        if keyword.lower() in answer_lower:
            matched_keywords.append(keyword)

    recall = len(matched_keywords) / len(expected_keywords)

    answer_words = set(
        predicted_answer.lower().split()
    )

    keyword_words = set(
        k.lower()
        for k in expected_keywords
    )

    precision = (
        len(keyword_words.intersection(answer_words))
        / max(len(answer_words), 1)
    )

    total_recall += recall
    total_precision += precision

    if recall > 0:
        successful_retrievals += 1

    print(f"\nExpected Keywords : {expected_keywords}")
    print(f"Matched Keywords  : {matched_keywords}")

    print(f"Recall            : {recall:.3f}")
    print(f"Precision         : {precision:.3f}")
    print(f"Query Time        : {query_time:.2f}s")

print("\n")
print("=" * 60)
print("FINAL RESULTS")
print("=" * 60)

success_rate = (
    successful_retrievals / total_questions
) * 100

avg_recall = (
    total_recall / total_questions
)

avg_precision = (
    total_precision / total_questions
)

avg_time = (
    total_time / total_questions
)

print(f"\nQuestions Tested      : {total_questions}")

print(
    f"Retrieval Success Rate: "
    f"{success_rate:.2f}%"
)

print(
    f"Average Recall        : "
    f"{avg_recall:.4f}"
)

print(
    f"Average Precision     : "
    f"{avg_precision:.4f}"
)

print(
    f"Average Query Time    : "
    f"{avg_time:.2f}s"
)