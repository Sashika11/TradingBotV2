
from core.ai_analysis import calculate_confidence
from core.risk import check_daily_loss
from execution.trade_router import route_trade
import pandas as pd

def main():
    trade_log = pd.read_csv("journal/trade_log.csv")
    allowed, pnl = check_daily_loss(trade_log)
    if not allowed:
        return
    ctx = {
        "liquidity_sweep": True,
        "bos": True,
        "trend": True,
        "session": True,
        "volatility": True
    }
    confidence = calculate_confidence(ctx)
    route_trade(ctx, confidence)

if __name__ == "__main__":
    main()
