def opposition_prompt(factor, support_text):
    return f"""
ROLE: Opponent

The Proponent said:
"{support_text}"

TASK:
- Attack EXACTLY ONE sentence or idea from the Proponent.
- Quote the sentence you are attacking.
- Explain why this single point weakens the claim.
- Do NOT introduce new benefits or multiple criticisms.
- Max 4 sentences. If you exceed this, your response is invalid.

Be critical, not verbose.
"""