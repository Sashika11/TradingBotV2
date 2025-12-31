def calculate_confidence(smc_ctx):
    """
    Returns AI confidence score (0-1)
    Example logic: trend + liquidity + FVG
    """
    score = 0.5
    if smc_ctx.get('trend') == 'BULLISH':
        score += 0.2
    if smc_ctx.get('liquidity_sweep_low') or smc_ctx.get('bull_fvg'):
        score += 0.2
    if smc_ctx.get('trend') == 'BEARISH':
        score -= 0.2
    if smc_ctx.get('liquidity_sweep_high') or smc_ctx.get('bear_fvg'):
        score -= 0.2
    # Clamp between 0 and 1
    return max(0, min(1, score))
