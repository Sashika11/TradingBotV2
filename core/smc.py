def analyze_smc(df):
    ctx = {}
    if df.empty:
        return ctx
    last = df.iloc[-1]
    high = df['High'].max()
    low = df['Low'].min()

    ctx['liquidity_sweep'] = last['High'] > high*0.98
    ctx['bos'] = last['Close'] < low*1.02
    ctx['trend'] = last['Close'] > df['Close'].mean()
    ctx['fvg'] = True
    ctx['volatility'] = True
    ctx['session'] = True
    ctx['Close'] = last['Close']
    return ctx
