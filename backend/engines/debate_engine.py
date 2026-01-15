from backend.agents.support_agent import SupportAgent
from backend.agents.oppose_agent import OppositionAgent
from backend.agents.moderator_agent import ModeratorAgent
from backend.core.schema import Factor


def run_debate(factor: Factor):
    support = SupportAgent()
    oppose = OppositionAgent()
    moderator = ModeratorAgent()

    # ---------- Round 1 ----------
    claim = support.round1(factor)
    attack = oppose.round1(factor, claim)

    # ---------- Round 2 ----------
    defense = support.round2(factor, claim, attack)
    counter = oppose.round2(factor, defense)

    # ---------- Internal transcript (ONLY for moderator) ----------
    transcript = (
        f"Claim: {claim}\n"
        f"Attack: {attack}\n"
        f"Defense: {defense}\n"
        f"Counter: {counter}"
    )

    # ---------- Moderator decision ----------
    decision = moderator.run(factor, transcript)

    # ---------- FINAL STRUCTURED OUTPUT ----------
    return {
        "factor": {
            "id": factor.id,
            "name": factor.name,
            "description": factor.description
        },
        "claim": claim.strip(),
        "attack": attack.strip(),
        "defense": defense.strip(),
        "counter": counter.strip(),
        "decision": decision
    }
