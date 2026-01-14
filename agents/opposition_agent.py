from prompts.opposition import opposition_prompt
from llm.groq_client import call_ollama

class OppositionAgent:
    def run(self, factor, transcript):
        return call_ollama(opposition_prompt(factor, transcript))
