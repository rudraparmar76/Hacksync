def opposition_round2_prompt(defense):
    return f"""
ROLE: Opponent

The Proponent defended their claim as follows:
"{defense}"

TASK:
- Explain why this defense is still insufficient OR unresolved.
- Max 2 sentences.

OUTPUT FORMAT:
\nCOUNTER: <your response>
"""
