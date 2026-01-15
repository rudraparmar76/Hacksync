import time
from datetime import datetime
from typing import Any, Dict, List, Optional


class TraceLogger:
    def __init__(self):
        self._trace: List[Dict[str, Any]] = []
        self._step_counter = 0
        self._start_time = time.time()

    def log_step(
        self,
        agent_name: str,
        input_data: Any = None,
        output_data: Any = None,
        factor_id: Optional[str] = None,
        factor_name: Optional[str] = None,
        stage: Optional[str] = None
    ):
        self._step_counter += 1

        self._trace.append({
            "step": self._step_counter,
            "agent": agent_name,
            "stage": stage,  # e.g. summarization, debate, synthesis
            "factor_id": factor_id,
            "factor_name": factor_name,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "elapsed_ms": int((time.time() - self._start_time) * 1000),
            "input": self._safe(input_data),
            "output": self._safe(output_data),
        })

    def get_trace(self) -> List[Dict[str, Any]]:
        return self._trace

    # ---------- helpers ----------

    def _safe(self, data: Any):
        if data is None:
            return None
        if isinstance(data, (str, int, float, bool)):
            return data
        if isinstance(data, (list, dict)):
            return data
        return str(data)
