from prompts.support import support_prompt
from llm.groq_client import call_ollama

class SupportAgent:
    def run(self, factor):
        return call_ollama(support_prompt(factor))
