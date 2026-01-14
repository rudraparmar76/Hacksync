import uuid
from datetime import datetime

class TraceLogger:
    def __init__(self):
        self.trace_id = str(uuid.uuid4())
        self.started_at = datetime.utcnow().isoformat()
        self.steps = []

    def log_step(self, agent_name: str, input_data, output_data):
        self.steps.append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": agent_name,
            "input": input_data,
            "output": output_data
        })

    def get_trace(self):
        return {
            "trace_id": self.trace_id,
            "started_at": self.started_at,
            "steps": self.steps
        }
