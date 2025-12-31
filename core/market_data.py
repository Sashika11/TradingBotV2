import os
import requests
import pandas as pd
from datetime import datetime

POLYGON_API_KEY = os.getenv('POLYGON_API_KEY')

def get_gold_data():
    url = f'https://api.polygon.io/v2/aggs/ticker/XAUUSD/prev?apiKey={POLYGON_API_KEY}'
    r = requests.get(url)
    data = r.json().get('results', [{}])[0]
    df = pd.DataFrame([data])
    df = df.rename(columns={'o':'Open','h':'High','l':'Low','c':'Close','v':'Volume'})
    df['time'] = pd.to_datetime(df.get('t', pd.Timestamp.now()), unit='ms')
    df = df.set_index('time')
    return df
