from typing import List, Dict

def build_prompt(query: str, chunks: List[Dict]) -> str:
    context = "\n\n".join([
        f"[Page {c['page']}] {c['text']}" for c in chunks
    ])

    prompt = f"""
You are an AI assistant answering questions based ONLY on the provided context.

Context:
{context}

Question:
{query}

Instructions:
- Answer ONLY from the context above
- If answer is not found, say "I don't know based on the provided document"
- Be concise and factual

Answer:
"""
    return prompt