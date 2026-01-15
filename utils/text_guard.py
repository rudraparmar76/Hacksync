import re

def enforce_sentence_limit(text, max_sentences):
    """
    Trims the text to a maximum number of sentences.
    Sentences are split on ., !, ?
    """
    if not text:
        return ""

    # Normalize whitespace
    text = text.strip()

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Keep only allowed number
    trimmed = sentences[:max_sentences]

    return " ".join(trimmed).strip()
