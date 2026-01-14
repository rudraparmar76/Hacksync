import os
import json
import re
from typing import Dict, List

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-2.5-flash"

SUMMARY_SCHEMA = {
    "summary": "string",
    "sections": [
        {
            "title": "string",
            "summary": "string"
        }
    ]
}


# ------------------ PUBLIC API ------------------

def summarize_document(normalized_input: Dict, max_chunk_size: int = 6000) -> Dict:
    """
    Summarizes multimodal input (text + structured insights)
    into a strict JSON analytical summary.
    """

    text = normalized_input.get("text", "").strip()
    structured_insights = normalized_input.get("structured_insights", [])

    if not text and not structured_insights:
        return {"summary": "", "sections": []}

    chunks = _chunk_text(text, max_chunk_size)

    chunk_summaries = []
    for idx, chunk in enumerate(chunks):
        chunk_summaries.append(_summarize_chunk(chunk, idx + 1))

    return _merge_summaries(chunk_summaries, structured_insights)


# ------------------ HELPERS ------------------

def _chunk_text(text: str, max_size: int) -> List[str]:
    return [text[i:i + max_size] for i in range(0, len(text), max_size)]


def _summarize_chunk(chunk: str, index: int) -> str:
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


def _merge_summaries(chunk_summaries: List[str], structured_insights: List[str]) -> Dict:
    model = genai.GenerativeModel(MODEL_NAME)

    joined_text = "\n\n".join(chunk_summaries)

    prompt = f"""
You are a deterministic summarization engine in a multimodal analysis system.

INPUTS:
- Natural language summaries
- Structured data insights (tables, metrics, charts)

TASK:
- Combine all inputs into a coherent analytical summary
- Treat structured insights as factual signals
- Do NOT invent data
- Do NOT speculate beyond provided inputs

CRITICAL OUTPUT RULES:
- Output ONLY valid JSON
- No markdown
- No explanations
- No text outside JSON
- Follow the schema EXACTLY

SCHEMA:
{json.dumps(SUMMARY_SCHEMA, indent=2)}

TEXT SUMMARIES:
{joined_text}

STRUCTURED INSIGHTS:
{json.dumps(structured_insights, indent=2)}
"""

    response = model.generate_content(prompt)
    return _safe_json_parse(response.text)


def _safe_json_parse(text: str) -> Dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {"summary": "", "sections": []}

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return {"summary": "", "sections": []}
