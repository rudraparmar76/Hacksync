import os
import json
import re
from typing import Dict

from dotenv import load_dotenv
import google.generativeai as genai

# ------------------ setup ------------------

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
 
# ⚡ Use Flash for lowest latency
MODEL_NAME = "gemini-2.5-flash"

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

def summarize_document(normalized_input: Dict) -> Dict:
    """
    FAST single-call summarization.
    Exactly ONE Gemini request per file.
    """

    text = normalized_input.get("text", "").strip()
    structured_insights = normalized_input.get("structured_insights", [])

    if not text and not structured_insights:
        return {"summary": "", "sections": []}

    # ---- light safety trim (prevents overload, keeps speed) ----
    MAX_CHARS = 18000  # safe for Gemini Flash
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]

    model = genai.GenerativeModel(MODEL_NAME)

    prompt = f"""
You are a document analysis engine.

The input may be long.

TASK:
1. Produce a concise overall summary (max 200 words)
2. Identify major sections or themes and summarize each
3. If the document is a worksheet or non-narrative, describe:
   - topics covered
   - structure
   - content or question types

RULES:
- Use ONLY the provided input
- Do NOT invent information
- Do NOT speculate
- Focus on themes, not line-by-line details

CRITICAL OUTPUT RULES:
- Output ONLY valid JSON
- No markdown
- No explanations
- No text outside JSON
- Follow the schema EXACTLY

SCHEMA:
{json.dumps(SUMMARY_SCHEMA, indent=2)}

DOCUMENT TEXT:
{text}

STRUCTURED INSIGHTS:
{json.dumps(structured_insights, indent=2)}

Limit total output to 300 words.
"""

    response = model.generate_content(prompt)
    return _safe_json_parse(response.text)

# ------------------ helpers ------------------

def _safe_json_parse(text: str) -> Dict:
    """
    Safely extract and parse JSON from Gemini output.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {"summary": "", "sections": []}

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return {"summary": "", "sections": []}
