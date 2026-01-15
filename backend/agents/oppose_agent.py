from backend.llm.groq_client import call_groq
from backend.prompts.opposition_round1 import opposition_round1_prompt
from backend.prompts.opposition_round2 import opposition_round2_prompt
from backend.utils.clean_text import clean_output
from backend.utils.text_guard import enforce_sentence_limit

class OppositionAgent:
    def round1(self, factor, claim_text):
        """
        Attack the initial claim, grounded in the factor context.
        """
        raw = call_groq(opposition_round1_prompt(factor, claim_text))
        return enforce_sentence_limit(clean_output(raw), 2)

    def round2(self, factor, defense_text):
        """
        Counter the defense, grounded in the factor context.
        """
        raw = call_groq(opposition_round2_prompt(factor, defense_text))
        return enforce_sentence_limit(clean_output(raw), 2)
