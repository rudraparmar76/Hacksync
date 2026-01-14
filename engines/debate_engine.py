from core.debate_state import DebateState
from agents.support_agent import SupportAgent
from agents.opposition_agent import OppositionAgent
from agents.moderator_agent import ModeratorAgent

def run_debate(factor):
    # 1. Initialize the Agents (Create instances)
    support_agent = SupportAgent()
    opposition_agent = OppositionAgent()
    moderator_agent = ModeratorAgent()

    # 2. Support Agent speaks
    # Now calling on the instance (support_agent) instead of the Class (SupportAgent)
    support_text = support_agent.run(factor)
    
    # 3. Opposition Agent sees Support's text
    oppose_text = opposition_agent.run(factor, support_text)
    
    # 4. Full Transcript for Moderator
    full_transcript = f"SUPPORT: {support_text}\n\nOPPOSITION: {oppose_text}"
    
    # 5. Moderator Decides
    decision = moderator_agent.run(factor, full_transcript)
    
    return {
        "transcript": full_transcript,
        "decision": decision
    }