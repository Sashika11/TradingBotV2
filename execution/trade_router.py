from alerts.telegram import send_alert
import os

# Switch between MANUAL / AUTO execution
MODE = os.getenv("TRADE_MODE", "MANUAL")

def route_trade(trade_decision, confidence):
    """
    Executes trade signal: sends Telegram alert, calculates Entry/SL/TP
    """
    if not trade_decision:
        print("No trade decision received.")
        return

    entry = trade_decision.get('entry_price', 0)
    sl = trade_decision.get('stop_loss', entry - 10)
    tp = trade_decision.get('take_profit', entry + 20)
    signal = trade_decision.get('signal', 'WAIT')
    reasoning = trade_decision.get('reasoning', 'No reason provided')

    msg = (
        f"📊 GOLD TRADE SIGNAL\n"
        f"Mode: {MODE}\n"
        f"Signal: {signal}\n"
        f"Entry: {entry}\n"
        f"SL: {sl}\n"
        f"TP: {tp}\n"
        f"Confidence: {confidence}\n"
        f"Reasoning: {reasoning}"
    )

    send_alert(msg)
    print(msg)
