def reciprocal_rank_fusion(dense_results, sparse_results, k=60):
    scores = {}

    def add_scores(results):
        for rank, item in enumerate(results):
            key = item["chunk_id"]
            scores.setdefault(key, 0)
            scores[key] += 1 / (k + rank + 1)

    add_scores(dense_results)
    add_scores(sparse_results)

    all_chunks = {c["chunk_id"]: c for c in dense_results + sparse_results}

    ranked = sorted(
        all_chunks.values(),
        key=lambda x: scores[x["chunk_id"]],
        reverse=True
    )


    for item in ranked:
        item["rrf_score"] = scores[item["chunk_id"]]
        

    return ranked