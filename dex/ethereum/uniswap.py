from web3 import Web3

ROUTER_ADDRESS = Web3.to_checksum_address("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")  # Uniswap V2 Router
TOKEN_OUT = Web3.to_checksum_address("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")     # USDC on Ethereum

def get_price(pair, web3):
    try:
        amount_in = web3.to_wei(1, 'ether')
        router = web3.eth.contract(address=ROUTER_ADDRESS, abi=[
            {"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],
             "inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},
                       {"internalType":"address[]","name":"path","type":"address[]"}],
             "stateMutability":"view","type":"function"}
        ])
        amounts = router.functions.getAmountsOut(amount_in, [Web3.to_checksum_address("0xC02aaa39b223FE8D0A0E5C4F27eAD9083C756Cc2"), TOKEN_OUT]).call()
        return amounts[-1] / (10 ** 6)
    except Exception as e:
        print(f"Error get_price ETH: {e}")
        return None

def execute_swap(web3, private_key, wallet_address, pair, amount_in_wei):
    try:
        wallet = Web3.to_checksum_address(wallet_address)
        web3.eth.default_account = wallet
        router = web3.eth.contract(address=ROUTER_ADDRESS, abi=[
            {"inputs":[
                {"internalType":"uint256","name":"amountOutMin","type":"uint256"},
                {"internalType":"address[]","name":"path","type":"address[]"},
                {"internalType":"address","name":"to","type":"address"},
                {"internalType":"uint256","name":"deadline","type":"uint256"}],
             "name":"swapExactETHForTokens",
             "outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],
             "stateMutability":"payable","type":"function"}
        ])
        nonce = web3.eth.get_transaction_count(wallet)
        tx = router.functions.swapExactETHForTokens(
            0,  # Accept any amountOut
            [wallet, TOKEN_OUT],
            wallet,
            web3.eth.get_block("latest")["timestamp"] + 60
        ).build_transaction({
            'from': wallet,
            'value': amount_in_wei,
            'gas': 300000,
            'gasPrice': web3.to_wei('30', 'gwei'),
            'nonce': nonce
        })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return web3.to_hex(tx_hash)
    except Exception as e:
        print(f"Error execute_swap ETH: {e}")
        return None
