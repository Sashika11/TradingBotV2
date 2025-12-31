import pandas as pd
from datetime import datetime

DAILY_LOSS_LIMIT = -50.0

def check_daily_loss(df):
    today = datetime.utcnow().date()
    today_trades = df[df['date'] == str(today)] if not df.empty else pd.DataFrame()
    daily_pnl = today_trades['pnl'].sum() if not today_trades.empty else 0
    return daily_pnl > DAILY_LOSS_LIMIT, daily_pnl
