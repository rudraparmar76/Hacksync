from llm.groq_client import call_ollama
from prompts.support_round1 import support_round1_prompt
from prompts.support_round2 import support_round2_prompt
from utils.clean_text import clean_output
from utils.text_guard import enforce_sentence_limit


class SupportAgent:
    def round1(self, factor):
        raw = call_ollama(support_round1_prompt(factor))
        return enforce_sentence_limit(clean_output(raw), 1)  # ONE claim sentence

    def round2(self, attack_text):
        raw = call_ollama(support_round2_prompt(attack_text))
        return enforce_sentence_limit(clean_output(raw), 2)  # short defense
