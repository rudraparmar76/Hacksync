def support_round1_prompt(factor):
    return f"""
ROLE: Proponent

TASK:
- State ONE clear claim based on the factor below.
- The claim must be ONE sentence only.

FACTOR:
{factor.description}

OUTPUT FORMAT:
\nCLAIM: <single sentence>
"""
