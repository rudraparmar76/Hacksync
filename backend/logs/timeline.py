from typing import List, Dict


def build_timeline(trace: List[Dict]) -> List[Dict]:
    """
    Converts trace logs into a clean timeline view.
    """
    timeline = []

    for entry in trace:
        timeline.append({
            "step": entry["step"],
            "agent": entry["agent"],
            "stage": entry.get("stage"),
            "factor": entry.get("factor_name"),
            "time_ms": entry["elapsed_ms"],
            "summary": _summarize_entry(entry)
        })

    return timeline


def _summarize_entry(entry: Dict) -> str:
    agent = entry["agent"]

    if agent == "Summarizer":
        return "Document summarized"
    if agent == "FactorAgent":
        return "Decision factors extracted"
    if agent == "DebateEngine":
        return f"Debate completed for {entry.get('factor_name')}"
    if agent == "SynthesizerAgent":
        return "Final decision synthesized"

    return f"{agent} executed"
