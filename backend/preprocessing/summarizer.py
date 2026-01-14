import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Dict, List

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"

def summarize_document(text: str, max_chunk_size: int = 6000) -> Dict:
    """
    Summarizes a potentially large document using Gemini.
    Uses chunking + hierarchical summarization.
    """

    if not text or len(text.strip()) == 0:
        return {
            "summary": "",
            "sections": []
        }

    chunks = _chunk_text(text, max_chunk_size)

    chunk_summaries = []
    for idx, chunk in enumerate(chunks):
        summary = _summarize_chunk(chunk, idx + 1)
        chunk_summaries.append(summary)

    final_summary = _merge_summaries(chunk_summaries)

    return final_summary

# ----------------------- helpers -----------------------

def _chunk_text(text: str, max_size: int) -> List[str]:
    """Split text into safe-size chunks"""
    chunks = []
    start = 0

    while start < len(text):
        end = start + max_size
        chunks.append(text[start:end])
        start = end

    return chunks


def _summarize_chunk(chunk: str, index: int) -> str:
    """Summarize a single chunk"""
    model = genai.GenerativeModel(MODEL_NAME)

    prompt = f"""
You are a professional analyst.

Summarize the following document chunk clearly and concisely.
Preserve important facts, metrics, decisions, and issues.
Do NOT add new information.
Do NOT speculate.

Chunk {index}:
{chunk}
"""

    response = model.generate_content(prompt)

    return response.text.strip()


def _merge_summaries(chunk_summaries: List[str]) -> Dict:
    """Merge chunk summaries into final structured output"""
    model = genai.GenerativeModel(MODEL_NAME)

    joined = "\n\n".join(chunk_summaries)

    prompt = f"""
You are synthesizing multiple summaries into a final structured overview.

Create:
1. A concise overall summary (max 250 words)
2. A list of key sections with short summaries

Return STRICT JSON ONLY in the following format:

{{
  "summary": "overall summary text",
  "sections": [
    {{
      "title": "Section title",
      "summary": "Section summary"
    }}
  ]
}}

Text:
{joined}
"""

    response = model.generate_content(prompt)

    # IMPORTANT: Gemini sometimes returns text before JSON
    # Simple safe extraction
    text = response.text.strip()
    json_start = text.find("{")
    json_end = text.rfind("}") + 1

    return eval(text[json_start:json_end])

