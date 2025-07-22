
import os
import requests

def send_telegram_alert(opportunity):
    try:
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not bot_token or not chat_id:
            print("⚠️ TELEGRAM no configurado.")
            return

        message = f"🔔 Arbitraje Detectado\nPar: {opportunity['pair']}\nBuy: {opportunity['buy_from']}\nSell: {opportunity['sell_to']}\nProfit: {opportunity['profit']}%"
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        requests.post(url, data={"chat_id": chat_id, "text": message})
    except Exception as e:
        print(f"❌ Error enviando alerta Telegram: {e}")
