def support_round1_prompt(factor):
    return f"""
ROLE: Proponent

FACTOR:
{factor.name} — {factor.description}

TASK:
- State ONE clear, defensible claim that supports this factor.
- The claim must be ONE sentence only.
- Do NOT hedge or list multiple points.

IMPORTANT:
- No labels
- No explanations
"""
