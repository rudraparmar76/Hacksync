def moderator_prompt(factor, transcript):
    return f"""
    Evaluate the debate below using these three criteria:
    1. Logical Consistency: Is the claim supported by the description?
    2. Feasibility: Can the risks mentioned be mitigated?
    3. Impact: Is the benefit significant enough to justify the effort?
    
    DEBATE: {transcript}
    
    SCORING GUIDE:
    1-3: Fundamentally flawed or too risky.
    4-6: Good idea, but has major implementation hurdles.
    7-9: Strong, actionable, and logical.
    10: Perfect (rare).
    
    OUTPUT JSON ONLY:
    {{
      "status": "ACCEPTED | REJECTED",
      "verdict": "Detailed logical conclusion.",
      "score": 1-10,
      "winning_argument": "Which specific logical point won the debate?"
    }}
    """