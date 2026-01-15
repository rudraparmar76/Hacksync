from typing import List, Dict


def build_trace_explanation(trace: List[Dict]) -> Dict:
    """
    Generates a human-readable explanation from trace.
    """

    explanation = {
        "factors_considered": [],
        "debates_run": 0,
        "final_decision_basis": []
    }

    for step in trace:
        if step["agent"] == "FactorAgent":
            for f in step["output"].get("factors", []):
                explanation["factors_considered"].append(f["name"])

        if step["agent"] == "DebateEngine":
            explanation["debates_run"] += 1

        if step["agent"] == "SynthesizerAgent":
            explanation["final_decision_basis"].append(
                "Final synthesis integrated all debate verdicts"
            )

    return explanation
