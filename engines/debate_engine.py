from agents.support_agent import SupportAgent
from agents.opposition_agent import OppositionAgent
from agents.moderator_agent import ModeratorAgent

def run_debate(factor):
    support = SupportAgent()
    oppose = OppositionAgent()
    moderator = ModeratorAgent()

    claim = support.round1(factor)
    attack = oppose.round1(claim)

    defense = support.round2(attack)
    counter = oppose.round2(defense)

    # Transcript ONLY for moderator (no emojis, no formatting)
    transcript = (
        f"Claim: {claim}\n"
        f"Attack: {attack}\n"
        f"Defense: {defense}\n"
        f"Counter: {counter}"
    )

    decision = moderator.run(factor, transcript)

    return {
        "claim": claim,
        "attack": attack,
        "defense": defense,
        "counter": counter,
        "decision": decision
    }
