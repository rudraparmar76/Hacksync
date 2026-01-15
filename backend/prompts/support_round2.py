def support_round2_prompt(factor, claim_text, attack_text):
    return f"""
ROLE: Proponent

FACTOR:
{factor.name} — {factor.description}

YOUR ORIGINAL CLAIM:
"{claim_text}"

OPPOSITION ATTACK:
"{attack_text}"

TASK:
- Defend or clarify the original claim in response to the attack.
- You may narrow the claim if needed.
- Do NOT introduce new examples, data, or arguments.
- Max 2 sentences.

IMPORTANT:
- Stay grounded in the factor
- No labels
"""
