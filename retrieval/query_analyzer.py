import re


def analyze_query(query: str):
    print("🟢QUERY : Analysing")
    """
    Analyze query characteristics
    """

    numbers = re.findall(r"\d+", query)

    keywords = [
        word.lower()
        for word in query.split()
        if len(word) > 3
    ]

    return {
        "numbers": numbers,
        "keywords": keywords,
        "query_length": len(query.split())
    }