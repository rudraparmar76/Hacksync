def opposition_round1_prompt(claim):
    return f"""
ROLE: Opponent

The Proponent made the following claim:
"{claim}"

TASK:
- Attack THIS claim directly.
- Identify ONE assumption or weakness.
- Max 2 sentences.

OUTPUT FORMAT:
\nATTACK: <your response>
"""
