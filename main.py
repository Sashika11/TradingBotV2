from core.market_data import get_gold_data
from core.smc import analyze_smc
from core.session_filter import valid_session
from core.risk import check_daily_loss
from core.ai_analysis import calculate_confidence
from execution.trade_router import route_trade
from alerts.telegram import send_alert
import pandas as pd

def main():
    trade_log_path = 'journal/trade_log.csv'
    if pd.io.common.file_exists(trade_log_path):
        trade_log = pd.read_csv(trade_log_path)
    else:
        trade_log = pd.DataFrame(columns=['date','pnl'])

    allowed, pnl = check_daily_loss(trade_log)
    if not allowed:
        send_alert(f"🛑 DAILY LOSS LOCK HIT\nPnL: ${pnl:.2f}\nTrading disabled until tomorrow.")
        return

    data = get_gold_data()
    smc_ctx = analyze_smc(data)

    if not valid_session():
        print("Outside trading session.")
        return

    confidence = calculate_confidence(smc_ctx)
    smc_ctx['confidence'] = confidence

    route_trade(smc_ctx, confidence)

if __name__ == "__main__":
    main()
