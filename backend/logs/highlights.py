from typing import List, Dict


def extract_decision_path(trace: List[Dict]) -> List[Dict]:
    """
    Returns only decision-critical steps.
    """
    highlights = []

    for step in trace:
        if step["agent"] in {
            "FactorAgent",
            "DebateEngine",
            "SynthesizerAgent"
        }:
            highlights.append({
                "step": step["step"],
                "agent": step["agent"],
                "factor": step.get("factor_name"),
                "output": step.get("output")
            })

    return highlights
