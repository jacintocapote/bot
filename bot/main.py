import sys
import os
import time
from dotenv import load_dotenv
from web3 import Web3

# Asegura que src esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.scanner import scan_prices
from utils.swapper import execute_trade
from utils.alert import send_telegram_alert

def load_environment():
    load_dotenv()

    # Múltiples RPCs
    rpc_endpoints = {
        "ethereum": os.getenv("RPC_URL"),
        "base": os.getenv("RPC_BASE"),
    }

    private_key = os.getenv("PRIVATE_KEY")
    wallet_address = os.getenv("WALLET_ADDRESS")

    if not private_key or not wallet_address:
        raise Exception("❌ Faltan variables en el archivo .env")

    web3_connections = {}
    for name, url in rpc_endpoints.items():
        if url:
            w3 = Web3(Web3.HTTPProvider(url))
            if not w3.is_connected():
                raise Exception(f"❌ No se pudo conectar a la red {name}")
            web3_connections[name] = w3
            print(f"✅ Conectado a {name} con {wallet_address}")

    return web3_connections, private_key, wallet_address

def run_bot():
    web3_connections, private_key, wallet_address = load_environment()

    while True:
        # Envía todas las conexiones a scanner
        opportunity = scan_prices(web3_connections)
        if opportunity:
            print(f"🔍 Spread detectado: {opportunity['profit']}% ({opportunity['buy_from']} -> {opportunity['sell_to']})")
            if opportunity['profit'] > 0.5:
                send_telegram_alert(opportunity)
                # Se asume que opportunity contiene el nombre de la red
                network = opportunity.get("network", "ethereum")
                web3 = web3_connections.get(network)
                if web3:
                    execute_trade(web3, private_key, wallet_address, opportunity)
                else:
                    print(f"⚠️ No se encontró conexión Web3 para la red: {network}")
            else:
                print(f"⛔ Oportunidad descartada: spread {opportunity['profit']}% < 0.5% mínimo requerido.")
        else:
            print("📉 No se detectó ninguna oportunidad de arbitraje en esta iteración.")
        time.sleep(10)

if __name__ == "__main__":
    run_bot()
