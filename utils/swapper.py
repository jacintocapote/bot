
from web3 import Web3
import json
import os

def execute_trade(web3, private_key, wallet_address, opportunity):
    try:
        with open("utils/uniswap_router_abi.json") as f:
            abi = json.load(f)

        router_address = Web3.to_checksum_address("0xE592427A0AEce92De3Edee1F18E0157C05861564")  # Uniswap V3 Router
        contract = web3.eth.contract(address=router_address, abi=abi)

        amount_in_wei = web3.to_wei(0.01, "ether")
        deadline = web3.eth.get_block("latest")["timestamp"] + 300

        tx = contract.functions.exactInputSingle({
            "tokenIn": web3.to_checksum_address("0xC02aaA39b223FE8D0A0E5C4F27eAD9083C756Cc2"),  # WETH
            "tokenOut": web3.to_checksum_address("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"),  # USDC
            "fee": 3000,
            "recipient": wallet_address,
            "deadline": deadline,
            "amountIn": amount_in_wei,
            "amountOutMinimum": 0,
            "sqrtPriceLimitX96": 0
        }).build_transaction({
            "from": wallet_address,
            "value": 0,
            "gas": 200000,
            "gasPrice": web3.to_wei("50", "gwei"),
            "nonce": web3.eth.get_transaction_count(wallet_address)
        })

        if os.getenv("MODE", "simulate").lower() == "live":
            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f"✅ Swap REAL enviado. Tx hash: {web3.to_hex(tx_hash)}")
        else:
            print("🧪 MODO SIMULACIÓN activado — transacción no enviada.")
            print(json.dumps(tx, indent=2))

    except Exception as e:
        print(f"❌ Error en execute_trade: {e}")
