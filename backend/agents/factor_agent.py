import os
import json
import re
from typing import Dict

from dotenv import load_dotenv
from groq import Groq

# ------------------ setup ------------------

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.1-8b-instant"

# ------------------ PUBLIC API ------------------

def run_factor_agent(summary_doc: Dict) -> Dict:
    prompt = f"""
You are a Factor Extraction Agent in a deliberative AI system.

INPUT:
You are given a summarized document consisting of:
- An overall summary
- Section-level summaries

TASK:
Extract 3–5 EVALUABLE DECISION FACTORS.

A factor MUST:
- Be debatable (can be argued for and against)
- Influence outcomes or decisions
- Be grounded in the provided summary

You MAY abstract evaluable factors from technical descriptions,
as long as they are grounded in the summary.

CRITICAL OUTPUT RULES:
- Output ONLY valid JSON
- No markdown
- No explanations
- Follow the schema EXACTLY

FORMAT:
{{
  "factors": [
    {{
      "id": "F1",
      "name": "string",
      "description": "string"
    }}
  ]
}}

DOCUMENT SUMMARY:
{json.dumps(summary_doc, indent=2)}

Limit total output to 200 tokens.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a JSON-only output engine."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=300
    )

    raw_text = response.choices[0].message.content
    print("Output: ",raw_text)
    return _safe_json_parse(raw_text)

# ------------------ helpers ------------------

def _safe_json_parse(text: str) -> Dict:
    try:
        return json.loads(text)
    except Exception:
        pass

    matches = re.findall(r"\{[\s\S]*?\}", text)
    for match in matches:
        try:
            parsed = json.loads(match)
            if "factors" in parsed:
                return parsed
        except Exception:
            continue

    return {"factors": []}
