from alerts.telegram import send_alert

MODE = 'MANUAL'

def route_trade(ctx, confidence):
    entry = ctx.get('Close', 0)
    sl = entry - 10
    tp = entry + 20
    msg = f"📊 GOLD TRADE SIGNAL\nMode: {MODE}\nEntry: {entry}\nSL: {sl}\nTP: {tp}\nConfidence: {confidence}\nContext: {ctx}"
    send_alert(msg)
