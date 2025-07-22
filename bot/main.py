
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
from dotenv import load_dotenv
from web3 import Web3

from utils.scanner import scan_prices
from utils.swapper import execute_trade
from utils.alert import send_telegram_alert

def load_environment():
    load_dotenv()

    rpc_url = os.getenv("RPC_URL")
    private_key = os.getenv("PRIVATE_KEY")
    wallet_address = os.getenv("WALLET_ADDRESS")

    if not rpc_url or not private_key or not wallet_address:
        raise Exception("❌ Faltan variables en el archivo .env")

    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise Exception("❌ No se pudo conectar a la red")

    print(f"✅ Conectado a la red con {wallet_address}")
    return web3, private_key, wallet_address

def run_bot():
    web3, private_key, wallet_address = load_environment()

    while True:
        opportunity = scan_prices(web3)
        if opportunity:
            print(f"🔍 Spread detectado: {opportunity['profit']}% ({opportunity['buy_from']} -> {opportunity['sell_to']})")
            if opportunity['profit'] > 0.5:
                send_telegram_alert(opportunity)
                execute_trade(web3, private_key, wallet_address, opportunity)
            else:
                print(f"⛔ Oportunidad descartada: spread {opportunity['profit']}% < 0.5% mínimo requerido.")
        else:
            print("📉 No se detectó ninguna oportunidad de arbitraje en esta iteración.")
        time.sleep(10)

if __name__ == "__main__":
    run_bot()
