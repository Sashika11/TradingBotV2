from groq import Groq
import os
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_ID = "llama-3.3-70b-versatile"

def ask_groq(smc_ctx, news="No major news"):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"""
    Act as a professional gold trader using SMC logic.
    DATA: {smc_ctx}
    NEWS: {news}
    Output JSON ONLY:
    {{
      "signal": "BUY/SELL/WAIT",
      "reasoning": "Technical reason",
      "confidence": {smc_ctx.get('confidence',0)}
    }}
    """
    try:
        completion = client.chat.completions.create(
            messages=[{"role":"user","content":prompt}],
            model=MODEL_ID,
            temperature=0.1,
            response_format={"type":"json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"Groq Error: {e}")
        return None
