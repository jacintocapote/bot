from web3 import Web3
import os
import requests

HELPER_CONTRACT = Web3.to_checksum_address("0xc0ba6c1eca707d8843bac10499f0a4b82e2ad67f")
TOKEN_OUT = Web3.to_checksum_address("0x4200000000000000000000000000000000000006")  # USDC on Base

def get_price(pair, web3=None):
    try:
        cmc_key = os.getenv("CMC_API_KEY")
        if not cmc_key:
            print("❌ Falta la CMC_API_KEY en el entorno")
            return None

        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        headers = {
            "X-CMC_PRO_API_KEY": cmc_key
        }

        params = {
            "symbol": "ETH",
            "convert": "USD"
        }

        response = requests.get(url, headers=headers, params=params)
        if not response.ok:
            print(f"❌ Error HTTP desde CoinMarketCap: {response.status_code}")
            return None

        data = response.json()
        price = float(data["data"]["ETH"]["quote"]["USD"]["price"])
        print(f"📊 Precio ETH/USD desde CoinMarketCap: {price}")
        return price

    except Exception as e:
        print(f"❌ Error get_price CMC: {e}")
        return None

def execute_swap(web3, private_key, wallet_address, pair, amount_in_wei):
    try:
        contract = web3.eth.contract(address=HELPER_CONTRACT, abi=[
            {
                "inputs": [
                    {"internalType": "address", "name": "tokenOut", "type": "address"},
                    {"internalType": "uint24", "name": "fee", "type": "uint24"}
                ],
                "name": "swapETHForToken",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "payable",
                "type": "function"
            }
        ])

        wallet = Web3.to_checksum_address(wallet_address)
        web3.eth.default_account = wallet
        nonce = web3.eth.get_transaction_count(wallet)

        tx = contract.functions.swapETHForToken(TOKEN_OUT, 3000).build_transaction({
            'from': wallet,
            'value': amount_in_wei,
            'gas': 300000,
            'gasPrice': web3.to_wei('1.5', 'gwei'),
            'nonce': nonce
        })

        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return web3.to_hex(tx_hash)

    except Exception as e:
        print(f"❌ Error execute_swap BASE: {e}")
        return None
