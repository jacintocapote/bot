from web3 import Web3

def has_sufficient_balance(web3: Web3, wallet_address: str, required_amount_wei: int) -> bool:
    try:
        balance = web3.eth.get_balance(wallet_address)
        if balance < required_amount_wei:
            eth = web3.from_wei(balance, 'ether')
            needed = web3.from_wei(required_amount_wei, 'ether')
            print(f"💸 Saldo insuficiente: tienes {eth} ETH, necesitas {needed} ETH")
            return False
        return True
    except Exception as e:
        print(f"❌ Error al comprobar saldo: {e}")
        return False
