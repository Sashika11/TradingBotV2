import pandas as pd
from datetime import datetime

def check_daily_loss(trade_log):
    today = datetime.now().date()
    today_trades = trade_log[trade_log['date'] == str(today)]
    daily_pnl = today_trades['pnl'].sum() if not today_trades.empty else 0
    limit = -50  # USD daily loss limit
    return daily_pnl > limit, daily_pnl
