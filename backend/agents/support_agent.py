import os
import json
import re
from typing import Dict

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"

SUPPORT_SCHEMA = {
    "claim": "string",
    "evidence": ["string"]
}


def run_support_agent(factor: Dict, document: Dict) -> Dict:
    """
    Argues FOR a given factor using evidence from the document.
    Returns STRICT JSON only.
    """

    model = genai.GenerativeModel(MODEL_NAME)

    prompt = f"""
You are a SUPPORTIVE reasoning agent in a multi-agent debate system.

ROLE:
Argue in FAVOR of the given factor.

WHAT YOU SHOULD DO:
- Assume the factor is valid
- Make a clear, confident claim
- Support it using evidence from the document
- Use facts, metrics, or observations from the text

WHAT YOU MUST NOT DO:
- Do NOT criticize the factor
- Do NOT hedge or weaken your claim
- Do NOT invent information
- Do NOT mention opposing viewpoints

OUTPUT RULES (CRITICAL):
- Output ONLY valid JSON
- No markdown
- No explanations
- Follow the schema EXACTLY

SCHEMA:
{json.dumps(SUPPORT_SCHEMA, indent=2)}

FACTOR:
{json.dumps(factor, indent=2)}

DOCUMENT SUMMARY:
{json.dumps(document, indent=2)}
"""

    response = model.generate_content(prompt)
    return _safe_json_parse(response.text)


# ------------------ helpers ------------------

def _safe_json_parse(text: str) -> Dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {"claim": "", "evidence": []}

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return {"claim": "", "evidence": []}
