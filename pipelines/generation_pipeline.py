from generation.prompt_builder import build_prompt
from generation.llm_client import generate_answer


def generate_response(
    query,
    retrieved_chunks
):
    """
    Full generation pipeline
    """

    # -----------------------------------
    # Build Prompt
    # -----------------------------------
    prompt = build_prompt(
        query=query,
        chunks=retrieved_chunks
    )

    # -----------------------------------
    # Generate Answer
    # -----------------------------------
    answer = generate_answer(prompt)

    return answer