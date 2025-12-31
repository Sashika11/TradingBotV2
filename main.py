import os
import pandas as pd
from datetime import datetime

# Core modules
from core.market_data import get_gold_data
from core.smc import analyze_smc
from core.session_filter import valid_session
from core.risk import check_daily_loss
from core.ai_analysis import calculate_confidence
from core.groq_analysis import ask_groq
from execution.trade_router import route_trade
from alerts.telegram import send_alert

TRADE_LOG_PATH = 'journal/trade_log.csv'

def load_trade_log():
    if os.path.exists(TRADE_LOG_PATH):
        return pd.read_csv(TRADE_LOG_PATH)
    else:
        return pd.DataFrame(columns=['date', 'pnl'])

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

    # 4️⃣ Session + volatility filter
    if not valid_session():
        print("Outside valid trading session.")
        return

    # 5️⃣ AI confidence scoring
    confidence = calculate_confidence(smc_ctx)
    smc_ctx['confidence'] = confidence

    # 6️⃣ Groq AI analysis for entry, stop loss, take profit, reasoning
    ai_decision = ask_groq(smc_ctx)
    if ai_decision:
        route_trade(ai_decision, ai_decision.get('confidence', confidence))
    else:
        print("⚠️ Groq AI analysis failed. No trade executed.")

if __name__ == "__main__":
    main()
