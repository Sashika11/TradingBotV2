def analyze_smc(df):
    """
    Simple SMC analysis: liquidity sweep, BOS, FVG, trend
    Returns dict with latest OHLC + SMC context
    """
    ctx = {}
    if df.empty:
        return ctx

    last = df.iloc[-1]
    ctx['Open'] = last['Open']
    ctx['High'] = last['High']
    ctx['Low'] = last['Low']
    ctx['Close'] = last['Close']

    # Trend via 200 EMA
    df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
    ctx['trend'] = "BULLISH" if last['Close'] > df['EMA_200'].iloc[-1] else "BEARISH"

    # Liquidity sweeps
    ctx['liquidity_sweep_high'] = last['High'] > df['High'].iloc[-2]
    ctx['liquidity_sweep_low'] = last['Low'] < df['Low'].iloc[-2]

    # Simple FVG detection (3-candle gap)
    ctx['bull_fvg'] = last['Low'] > df['High'].shift(2).iloc[-1]
    ctx['bear_fvg'] = last['High'] < df['Low'].shift(2).iloc[-1]

    return ctx
