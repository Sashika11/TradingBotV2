import pandas as pd

def analyze_smc(df: pd.DataFrame):
    """
    Simple SMC analysis: liquidity sweep, BOS, FVG, trend
    Returns dict with latest OHLC + SMC context
    """
    ctx = {}
    if df.empty or len(df) < 3:
        return ctx  # Not enough data for FVG or liquidity checks

    # Add EMA_200 first
    df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()

    # Last row as a scalar Series
    last = df.iloc[-1]

    # OHLC
    ctx['Open'] = last['Open']
    ctx['High'] = last['High']
    ctx['Low'] = last['Low']
    ctx['Close'] = last['Close']

    # Trend via 200 EMA
    ctx['trend'] = "BULLISH" if last['Close'] > last['EMA_200'] else "BEARISH"

    # Liquidity sweeps (compare scalars)
    prev = df.iloc[-2]
    ctx['liquidity_sweep_high'] = last['High'] > prev['High']
    ctx['liquidity_sweep_low'] = last['Low'] < prev['Low']

    # Simple FVG detection (3-candle gap)
    prev2 = df.iloc[-3]
    ctx['bull_fvg'] = last['Low'] > prev2['High']
    ctx['bear_fvg'] = last['High'] < prev2['Low']

    # Break of Structure (BOS)
    # Bullish BOS: last close breaks above previous swing high
    swing_high = df['High'].iloc[:-1].max()  # Max high excluding last candle
    # Bearish BOS: last close breaks below previous swing low
    swing_low = df['Low'].iloc[:-1].min()    # Min low excluding last candle

    ctx['bull_bos'] = last['Close'] > swing_high
    ctx['bear_bos'] = last['Close'] < swing_low

    return ctx
