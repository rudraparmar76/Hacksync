def support_prompt(factor):
    return f"""
    Analyze the following factor from a growth perspective:
    FACTOR: {factor.name}
    DESCRIPTION: {factor.description}
    
    TASK:
    1. Identify the primary value proposition.
    2. Provide a logical explanation of how this factor leads to a successful outcome.
    3. Use data-driven reasoning based on the provided description.
    
    STRICT: No marketing jargon. Focus on technical and logical benefits.
    """