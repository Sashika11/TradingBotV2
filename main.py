def main():
    trade_log = load_trade_log()

    # 1️⃣ Check daily loss limit
    allowed, daily_pnl = check_daily_loss(trade_log)
    if not allowed:
        send_alert(f"🛑 DAILY LOSS LOCK HIT\nPnL: ${daily_pnl:.2f}\nTrading disabled until tomorrow.")
        return

    # 2️⃣ Get gold market data
    df = get_gold_data()
    if df.empty:
        print("⚠️ Failed to fetch market data.")
        return

    # 3️⃣ Analyze SMC (liquidity sweep, BOS, FVG, trend)
    smc_ctx = analyze_smc(df)
    print("SMC Context:", smc_ctx)  # optional debugging

    # 4️⃣ Session + volatility filter
    if not valid_session():
        print("Outside valid trading session.")
        return

    # 5️⃣ AI confidence scoring
    confidence = calculate_confidence(smc_ctx)

    # 🔹 Adjust confidence based on SMC signals
    # Trend alignment
    if smc_ctx.get('trend') == 'BULLISH':
        confidence += 0.05
    else:
        confidence -= 0.05

    # Break of Structure (BOS)
    if smc_ctx.get('bull_bos'):
        confidence += 0.1
    if smc_ctx.get('bear_bos'):
        confidence -= 0.1

    # Liquidity sweeps
    if smc_ctx.get('liquidity_sweep_high'):
        confidence += 0.05
    if smc_ctx.get('liquidity_sweep_low'):
        confidence -= 0.05

    # Fair Value Gaps (FVG)
    if smc_ctx.get('bull_fvg'):
        confidence += 0.05
    if smc_ctx.get('bear_fvg'):
        confidence -= 0.05

    # Clip confidence to [0,1]
    confidence = max(0, min(1, confidence))
    smc_ctx['confidence'] = confidence

    # 6️⃣ Groq AI analysis for entry, stop loss, take profit, reasoning
    ai_decision = ask_groq(smc_ctx)
    if ai_decision:
        route_trade(ai_decision, ai_decision.get('confidence', confidence))
    else:
        print("⚠️ Groq AI analysis failed. No trade executed.")
