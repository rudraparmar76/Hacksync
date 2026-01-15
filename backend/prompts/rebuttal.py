def rebuttal_prompt(opposition_text):
    return f"""
ROLE: Proponent (Rebuttal)

The Opponent argued:
"{opposition_text}"

TASK:
- Respond ONLY to this criticism.
- You may defend OR partially concede and narrow the claim.
- You may NOT introduce new data, examples, or studies.
- Max 3 sentences. If you exceed this, your response is invalid.

Stay disciplined.
"""