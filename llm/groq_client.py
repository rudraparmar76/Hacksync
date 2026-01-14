import os
from groq import Groq

# 🔑 Use the new production model ID
# "llama-3.3-70b-versatile" is the current state-of-the-art on Groq
MODEL_ID = "openai/gpt-oss-120b"
GROQ_API_KEY = "api_key" # REMEMBER: Create a new key in Groq console!

client = Groq(api_key=GROQ_API_KEY)

def call_ollama(prompt: str) -> str:
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
                full_response += text
        
        return full_response.strip()

    except Exception as e:
        print(f"\n❌ Groq API Error: {e}")
        return f"Error: {str(e)}"