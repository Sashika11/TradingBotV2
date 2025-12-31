import os
import requests
import pandas as pd
import yfinance as yf
from datetime import datetime

POLYGON_API_KEY = os.getenv('POLYGON_API_KEY')

def get_gold_data():
    """
    Fetch gold market data for trading bot.
    Primary: Polygon.io (free tier)
    Fallback: Yahoo Finance
    Returns: pandas DataFrame with OHLCV and datetime index
    """
    df = pd.DataFrame()
    
    # --- 1️⃣ Try Polygon API ---
    if POLYGON_API_KEY:
        try:
            url = f'https://api.polygon.io/v2/aggs/ticker/C:XAUUSD/prev?apiKey={POLYGON_API_KEY}'
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json().get('results', [])
                if data:
                    df = pd.DataFrame(data)
                    df = df.rename(columns={
                        'o': 'Open',
                        'h': 'High',
                        'l': 'Low',
                        'c': 'Close',
                        'v': 'Volume',
                        't': 'time'
                    })
                    df['time'] = pd.to_datetime(df['time'], unit='ms')
                    df = df.set_index('time')
                    print(f"✅ Polygon data fetched: {len(df)} rows")
                    return df
                else:
                    print("⚠️ Polygon returned no data")
            else:
                print(f"⚠️ Polygon API error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"⚠️ Polygon fetch exception: {e}")

    # --- 2️⃣ Fallback to Yahoo Finance ---
    try:
        df = yf.download("GC=F", period="1mo", interval="1h", progress=False)
        if not df.empty:
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
            print(f"✅ Yahoo Finance fallback used: {len(df)} rows")
            return df
        else:
            print("⚠️ Yahoo Finance returned no data")
    except Exception as e:
        print(f"⚠️ Yahoo Finance fetch exception: {e}")

    # --- 3️⃣ If all fails, return empty DataFrame ---
    print("❌ Failed to fetch any market data")
    return df
