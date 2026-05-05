import re

def clean_text(text: str) -> str:
    """
    Basic text cleaning:
    - remove extra spaces
    - remove newlines
    """
    text = re.sub(r"\s+", " ", text)
    return text.strip()