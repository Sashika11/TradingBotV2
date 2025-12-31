import os
import requests

def send_alert(msg):
    token = os.getenv('TELEGRAM_TOKEN')
    chat = os.getenv('TELEGRAM_CHAT_ID')
    if token and chat:
        requests.post(f'https://api.telegram.org/bot{token}/sendMessage', data={'chat_id': chat, 'text': msg})
    else:
        print(msg)
