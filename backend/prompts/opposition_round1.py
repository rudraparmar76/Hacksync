def opposition_round1_prompt(factor, claim_text):
    return f"""
ROLE: Opposition

FACTOR:
{factor.name} — {factor.description}

PROPONENT CLAIM:
"{claim_text}"

TASK:
- Directly challenge the claim.
- Identify ONE flawed assumption, gap, or weakness.
- Stay grounded in the factor context.
- Max 2 sentences.

IMPORTANT:
- Do NOT repeat the claim.
- Do NOT introduce multiple criticisms.
"""
