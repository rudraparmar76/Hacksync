from typing import List, Dict


def filter_trace_by_factor(trace: List[Dict], factor_id: str) -> List[Dict]:
    return [
        step for step in trace
        if step.get("factor_id") == factor_id
    ]

# Usage
# factor_trace = filter_trace_by_factor(full_trace, "F1")
