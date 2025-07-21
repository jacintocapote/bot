import time
from utils.scanner import scan_prices
from utils.swapper import execute_trade
from utils.alert import send_telegram_alert

def run_bot():
    while True:
        opportunity = scan_prices()
        if opportunity and opportunity['profit'] > 0.5:
            send_telegram_alert(opportunity)
            execute_trade(opportunity)
        time.sleep(10)

if __name__ == "__main__":
    run_bot()
