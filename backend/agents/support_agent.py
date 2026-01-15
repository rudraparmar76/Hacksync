from backend.llm.groq_client import call_groq
from backend.prompts.support_round1 import support_round1_prompt
from backend.prompts.support_round2 import support_round2_prompt
from backend.utils.clean_text import clean_output
from backend.utils.text_guard import enforce_sentence_limit


class SupportAgent:
    def round1(self, factor):
        """
        Produce a single concise claim supporting the factor.
        """
        raw = call_groq(support_round1_prompt(factor))
        return enforce_sentence_limit(clean_output(raw), 1)

    def round2(self, factor, claim_text, attack_text):
        """
        Defend the original claim against the opposition attack.
        """
        raw = call_groq(
            support_round2_prompt(
                factor=factor,
                claim_text=claim_text,
                attack_text=attack_text
            )
        )
        return enforce_sentence_limit(clean_output(raw), 2)
