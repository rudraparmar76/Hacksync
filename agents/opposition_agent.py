from llm.groq_client import call_ollama
from prompts.opposition_round1 import opposition_round1_prompt
from prompts.opposition_round2 import opposition_round2_prompt
from utils.clean_text import clean_output
from utils.text_guard import enforce_sentence_limit


class OppositionAgent:
    def round1(self, claim_text):
        raw = call_ollama(opposition_round1_prompt(claim_text))
        return enforce_sentence_limit(clean_output(raw), 2)

    def round2(self, defense_text):
        raw = call_ollama(opposition_round2_prompt(defense_text))
        return enforce_sentence_limit(clean_output(raw), 2)
