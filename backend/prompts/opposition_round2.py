def opposition_round2_prompt(factor, defense_text):
    return f"""
ROLE: Opposition

FACTOR:
{factor.name} — {factor.description}

PROPONENT DEFENSE:
"{defense_text}"

TASK:
- Explain why the defense does NOT fully resolve the original weakness.
- Point out what remains unaddressed or unsupported.
- Max 2 sentences.

IMPORTANT:
- Be precise.
- Do NOT introduce new arguments.
"""
