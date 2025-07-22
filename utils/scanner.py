import requests

def scan_prices(web3):
    try:
        # Dexscreener pair URLs (Uniswap y Sushiswap ETH/USDC)
        uniswap_resp = requests.get("https://api.dexscreener.com/latest/dex/pairs/ethereum/0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc")
        sushiswap_resp = requests.get("https://api.dexscreener.com/latest/dex/pairs/ethereum/0x397FF1542f962076d0BFE58eA045FfA2d347ACa0")

        if not uniswap_resp.ok or not sushiswap_resp.ok:
            print("❌ Error al obtener precios de Dexscreener")
            return None

        uni_price = float(uniswap_resp.json()['pair']['priceUsd'])
        sushi_price = float(sushiswap_resp.json()['pair']['priceUsd'])

        print(f"🧪 Precios obtenidos:")
        print(f"   Uniswap:   {uni_price}")
        print(f"   Sushiswap: {sushi_price}")

        profit = abs(uni_price - sushi_price) / min(uni_price, sushi_price) * 100
        print(f"🔍 Spread calculado: {profit:.6f}%")

        if profit >= 0.5:
            return {
                "profit": round(profit, 6),
                "pair": "ETH/USDC",
                "buy_from": "Uniswap" if uni_price < sushi_price else "Sushiswap",
                "sell_to": "Sushiswap" if uni_price < sushi_price else "Uniswap",
                "buy_price": min(uni_price, sushi_price),
                "sell_price": max(uni_price, sushi_price)
            }

        print(f"⛔ Spread {profit:.6f}% inferior al umbral mínimo (0.5%)")
        return None

    except Exception as e:
        print(f"❌ Error en scan_prices: {e}")
        return None
