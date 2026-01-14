def opposition_prompt(factor, transcript):
    return f"""
    Critically audit the following claim: "{transcript}"
    
    TASK:
    1. Identify one specific logistical, financial, or cognitive risk.
    2. Explain why this risk might outweigh the benefits mentioned.
    3. Do not ignore the benefits; instead, explain why they are difficult to sustain.
    """