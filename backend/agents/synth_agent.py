import os
import json
import re
from typing import List, Dict
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.1-8b-instant"


# ------------------ public API ------------------

def run_synth_agent(debate_results: List[Dict]) -> Dict:
    """
    Deterministic synthesis over structured debate results.
    """

    compact_debates = _compact_debates(debate_results)
    prompt = _build_prompt(compact_debates)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a synthesis engine. "
                    "You MUST output STRICT JSON only. "
                    "No explanations, no markdown."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=900
    )

    raw_text = response.choices[0].message.content
    return _safe_json_parse(raw_text)


# ------------------ prompt ------------------

def _build_prompt(debates: List[Dict]) -> str:
    return f"""
You are synthesizing results from a multi-agent debate system.

INPUT:
Each debate contains:
- factor (name + description)
- claim, attack, defense, counter
- final decision (status, verdict, score, winning_argument)

TASK:
Produce a FINAL INTEGRATED REPORT.

YOU MUST EXPLICITLY ANSWER:
1. What worked
2. What failed
3. Why it happened
4. How to improve

GUIDELINES:
- Respect moderator decisions
- Weigh debates with higher scores more heavily
- Identify patterns across factors
- Do NOT invent new arguments
- Do NOT repeat debate text verbatim

CRITICAL OUTPUT RULES:
- Output ONLY valid JSON
- Follow the schema EXACTLY
- No text outside JSON

OUTPUT SCHEMA:
{{
  "executive_summary": "Overall conclusion across all debates",
  "why_this_decision": "How debate verdicts and scores led to this outcome",

  "what_worked": [
    "Successful reasoning pattern or factor"
  ],
  "what_failed": [
    "Failed assumption or weak reasoning"
  ],
  "why_it_happened": "Root cause explanation based on debates",
  "how_to_improve": [
    {{
      "improvement": "Concrete improvement",
      "justification": "Why this addresses the failure"
    }}
  ],

  "key_insights": [
    "Cross-factor insight"
  ],
  "strategic_recommendations": [
    {{
      "strategy": "Strategy name",
      "action": "Action to take",
      "rationale": "Grounded in debate outcomes"
    }}
  ],
  "risk_assessment": "Risks identified from opposition and counters"
}}

DEBATE RESULTS:
{json.dumps(debates, indent=2)}

Limit total output to 350 tokens.
"""


# ------------------ helpers ------------------

def _compact_debates(debates: List[Dict], max_chars: int = 4000) -> List[Dict]:
    """
    Prevent token overload by trimming long text fields.
    """
    text = json.dumps(debates)
    if len(text) <= max_chars:
        return debates

    trimmed = []
    for d in debates:
        trimmed.append({
            "factor": d["factor"],
            "claim": d["claim"][:300],
            "attack": d["attack"][:300],
            "defense": d["defense"][:300],
            "counter": d["counter"][:300],
            "decision": d["decision"]
        })

    return trimmed


def _safe_json_parse(text: str) -> Dict:
    """
    Robust JSON extraction.
    """
    try:
        return json.loads(text)
    except Exception:
        pass

    matches = re.findall(r"\{[\s\S]*?\}", text)
    for m in matches:
        try:
            parsed = json.loads(m)
            if "executive_summary" in parsed:
                return parsed
        except Exception:
            continue

    return {
        "executive_summary": "Synthesis failed.",
        "why_this_decision": "Model did not return valid structured output.",
        "what_worked": [],
        "what_failed": [],
        "why_it_happened": "Unknown",
        "how_to_improve": [],
        "key_insights": [],
        "strategic_recommendations": [],
        "risk_assessment": "Unknown"
    }
