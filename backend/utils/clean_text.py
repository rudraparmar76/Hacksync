import re

def clean_output(text):
    """
    Cleans LLM output and enforces debate-friendly formatting.
    """
    if not text:
        return ""

    # Remove markdown symbols
    text = re.sub(r'[`*_>#]', '', text)

    # Force line breaks before debate labels (even if glued)
    labels = ["CLAIM", "ATTACK", "DEFENSE", "COUNTER"]
    for label in labels:
        text = re.sub(rf"\s*{label}\s*:", f"\n{label}:", text, flags=re.IGNORECASE)

    # Remove labels themselves (we add them in main.py)
    text = re.sub(r'\b(CLAIM|ATTACK|DEFENSE|COUNTER)\s*:\s*', '', text, flags=re.IGNORECASE)

    # Remove JSON if model leaked verdict
    text = re.sub(r'\{.*?\}', '', text, flags=re.DOTALL)

    # Normalize whitespace
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()