import sys
import os
import time
from dotenv import load_dotenv
from web3 import Web3

from scan_prices import scan_prices
from execute_trade import execute_trade
from utils.alert import send_telegram_alert
from utils.wallet import has_sufficient_balance

def load_environment():
    load_dotenv()

    mode = os.getenv("MODE", "simulate")
    private_key = os.getenv("PRIVATE_KEY")
    wallet_address = os.getenv("WALLET_ADDRESS")

    web3_connections = {
        "ethereum": Web3(Web3.HTTPProvider(os.getenv("RPC_ETHEREUM"))),
        "base": Web3(Web3.HTTPProvider(os.getenv("RPC_BASE"))),
    }

    for name, w3 in web3_connections.items():
        if not w3.is_connected():
            raise Exception(f"❌ No se pudo conectar a {name}")
        else:
            print(f"✅ Conectado a {name}")

    return web3_connections, private_key, wallet_address, mode

def run_bot():
    web3_connections, private_key, wallet_address, mode = load_environment()

    while True:
        opportunity = scan_prices(web3_connections)
        if opportunity:
            print(f"🔍 Spread detectado: {opportunity['profit']}% ({opportunity['buy_from']} -> {opportunity['sell_to']})")
            if opportunity['profit'] >= 0.5:
                send_telegram_alert(opportunity)
                amount_in_wei = web3_connections[opportunity['network']].to_wei(0.01, 'ether')

                web3 = web3_connections[opportunity['network']]
                if has_sufficient_balance(web3, wallet_address, amount_in_wei):
                  if mode == "live":
                    execute_trade(web3_connections, private_key, wallet_address, opportunity)
                  else:
                    print("🧪 Simulación de swap ejecutada (no real)")
                else:
                  print("⛔ Swap cancelado por saldo insuficiente")

            else:
                print(f"⛔ Oportunidad descartada: spread {opportunity['profit']}% < 0.5% mínimo requerido.")
        else:
            print("📉 No se detectó ninguna oportunidad de arbitraje en esta iteración.")
        time.sleep(10)

if __name__ == "__main__":
    run_bot()
