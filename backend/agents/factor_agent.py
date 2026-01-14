import os
import json
import re
from typing import Dict, List

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"

FACTOR_SCHEMA = {
    "factors": [
        {
            "id": "string (F1, F2, ...)",
            "name": "string",
            "description": "string"
        }
    ]
}


def run_factor_agent(document: Dict) -> Dict:
    """
    Extracts evaluable decision factors from a summarized document.
    Returns STRICT JSON only.
    """

    model = genai.GenerativeModel(MODEL_NAME)

    prompt = f"""
You are a senior analytical agent in a multi-agent decision system.

TASK:
Extract the most important EVALUABLE FACTORS from the document.

DEFINITION OF A FACTOR:
- A dimension that can be argued FOR and AGAINST
- Relevant to decision-making
- Supported by information in the document
- Not a keyword, not a section title

RULES:
- Extract 3 to 6 factors
- Do NOT invent information
- Do NOT repeat similar factors
- Do NOT include trivial or descriptive points

OUTPUT RULES (CRITICAL):
- Output ONLY valid JSON
- No markdown
- No explanations
- Follow the schema EXACTLY

SCHEMA:
{json.dumps(FACTOR_SCHEMA, indent=2)}

DOCUMENT SUMMARY:
{json.dumps(document, indent=2)}
"""

    response = model.generate_content(prompt)

    return _safe_json_parse(response.text)


# ------------------ helpers ------------------

def _safe_json_parse(text: str) -> Dict:
    """
    Safely extract and parse JSON from LLM output.
    Never executes code.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {"factors": []}

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return {"factors": []}
