from groq import Groq
import os
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_ID = "llama-3.3-70b-versatile"

def ask_groq(smc_ctx, news="No major news"):
    """
    Sends SMC context and optional news to Groq AI
    Returns AI trade decision: Entry, SL, TP, signal, reasoning, confidence
    """
    if not GROQ_API_KEY:
        print("⚠️ Groq API key not set")
        return None

    try:
        client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        print(f"❌ Groq initialization error: {e}")
        return None

    prompt = f"""
    Act as a professional gold trader using SMC logic.

    DATA:
    {smc_ctx}

    NEWS:
    {news}

    STRICT ENTRY RULES:
    1. BUY IF: Trend is BULLISH + Liquidity Sweep Low OR inside Bullish FVG
    2. SELL IF: Trend is BEARISH + Liquidity Sweep High OR inside Bearish FVG
    3. WAIT IF: No Sweep and No FVG test

    Output JSON ONLY:
    {{
        "signal": "BUY/SELL/WAIT",
        "reasoning": "Technical reason",
        "entry_price": {smc_ctx.get("Close",0)},
        "stop_loss": {smc_ctx.get("Close",0)-10},
        "take_profit": {smc_ctx.get("Close",0)+20},
        "confidence": {smc_ctx.get("confidence",0)}
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
        print(f"❌ Groq AI error: {e}")
        return None
