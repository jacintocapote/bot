
from web3 import Web3

def execute_trade(web3_connections, private_key, wallet_address, opportunity, amount_eth=0.01):
    try:
        pair = opportunity["pair"]
        network = opportunity["network"]

        if network not in web3_connections:
            print(f"❌ Red {network} no está conectada.")
            return

        web3 = web3_connections[network]
        amount_in_wei = web3.to_wei(amount_eth, 'ether')

        # Importar el módulo dinámicamente
        dex_module = __import__(f"dex.{network}.uniswap", fromlist=["execute_swap"])

        print(f"⚡ Ejecutando swap {pair} en {network}")
        tx_hash = dex_module.execute_swap(web3, private_key, wallet_address, pair, amount_in_wei)
        print(f"✅ Swap ejecutado: {tx_hash}")
        return tx_hash

    except Exception as e:
        print(f"❌ Error en execute_trade: {e}")
        return None
