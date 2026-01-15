import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
MODEL_ID = "openai/gpt-oss-120b"
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def call_groq(prompt: str) -> str:
    """
    Calls Groq Cloud while maintaining the 'call_ollama' interface 
    for backward compatibility with your existing agents.
    """
    try:
        completion = client.chat.completions.create(
            model=MODEL_ID, 
            messages=[
                {"role": "system", "content": "You are a logical debate assistant. Provide concise, sharp arguments."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0, # Lower temp for more logical/consistent debate
            max_tokens=1024,
            stream=True
        )

        full_response = ""
        # We use flush=True so the text 'flows' into the terminal character-by-character
        for chunk in completion:
            if chunk.choices[0].delta.content:
                text = chunk.choices[0].delta.content
                print(text, end="", flush=True)
                time.sleep(0.05)
                full_response += text
        
        return full_response.strip()

    except Exception as e:
        print(f"\n❌ Groq API Error: {e}")
        return f"Error: {str(e)}"