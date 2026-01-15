from prompts.moderator import moderator_prompt
from llm.groq_client import call_ollama
import json
import re

class ModeratorAgent:
    def run(self, factor, transcript):
        response = call_ollama(moderator_prompt(factor, transcript))

        try:
            match = re.search(r"\{.*\}", response, re.DOTALL)
            if not match:
                raise ValueError("No JSON found")

            return json.loads(match.group(0))
        except Exception:
            return {
                "status": "REJECTED",
                "verdict": "Moderator could not reliably evaluate the debate.",
                "score": 0,
                "winning_argument": "Evaluation failure"
            }
