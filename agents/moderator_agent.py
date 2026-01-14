from prompts.moderator import moderator_prompt
from llm.groq_client import call_ollama
import json
import re

class ModeratorAgent:
    def run(self, factor, transcript): # Added 'self'
        prompt = moderator_prompt(factor, transcript)
        response = call_ollama(prompt)
        
        try:
            # DOTALL is essential because JSON usually spans multiple lines
            match = re.search(r"\{.*\}", response, re.DOTALL)
            if match:
                json_str = match.group(0)
                # Clean up potential markdown code blocks like ```json ... ```
                json_str = json_str.replace("```json", "").replace("```", "")
                return json.loads(json_str)
            else:
                raise ValueError("No JSON block found")
                
        except (json.JSONDecodeError, ValueError) as e:
            # Log the error but return a valid dictionary so the main loop doesn't crash
            print(f"⚠️ Moderator formatting error. Attempting fallback.")
            return {
                "status": "REJECTED",
                "reasoning": f"Failed to parse model response. Error: {str(e)}",
                "score": 0
            }