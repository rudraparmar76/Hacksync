def support_round2_prompt(attack):
    return f"""
ROLE: Proponent

The Opponent attacked your claim:
"{attack}"

TASK:
- Defend the original claim against THIS attack.
- You may clarify or narrow the claim.
- Do NOT introduce new examples or data.
- Max 2 sentences.

OUTPUT FORMAT:
\nDEFENSE: <your response>
"""
