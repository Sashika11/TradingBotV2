def calculate_confidence(ctx):
    score = 0
    score += 0.3 if ctx.get('liquidity_sweep') else 0
    score += 0.25 if ctx.get('bos') else 0
    score += 0.2 if ctx.get('trend') else 0
    score += 0.15 if ctx.get('session') else 0
    score += 0.1 if ctx.get('volatility') else 0
    return round(score,2)
