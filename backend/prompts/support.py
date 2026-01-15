def support_prompt(factor):
    return f"""
ROLE: Proponent

CLAIM:
"{factor.description}"

RULES:
- Make ONE clear argument only.
- State ONE concrete benefit.
- Do NOT mention risks or limitations.
- Max 4 sentences. If you exceed this, your response is invalid.

Be direct and precise.
"""