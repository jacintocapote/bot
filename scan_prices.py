
import yaml
from web3 import Web3

def scan_prices(web3_connections):
    try:
        with open("config/pairs.yaml", "r") as f:
            config = yaml.safe_load(f)

        for pair_cfg in config["pairs"]:
            pair_name = pair_cfg["name"]
            sources = pair_cfg["sources"]
            if len(sources) != 2:
                print(f"⚠️ Pares no soportados: {pair_name}")
                continue

            # Cargar módulos dinámicamente
            prices = []
            for source in sources:
                network = source["network"]
                dex_name = source["dex"]

                module = __import__(f"dex.{network}.{dex_name}", fromlist=["get_price"])
                web3 = web3_connections[network]
                price = module.get_price(pair_name, web3)
                prices.append((network, dex_name, price))

            # Comparar precios
            (n1, d1, p1), (n2, d2, p2) = prices
            if not p1 or not p2:
                print("❌ Precios no disponibles")
                continue

            print(f"🧪 {pair_name} → {d1}@{n1}: {p1}, {d2}@{n2}: {p2}")
            spread = abs(p1 - p2) / min(p1, p2) * 100

            if spread >= 0.5:
                buy_from = (n1, d1, p1) if p1 < p2 else (n2, d2, p2)
                sell_to  = (n2, d2, p2) if p1 < p2 else (n1, d1, p1)
                return {
                    "pair": pair_name,
                    "profit": round(spread, 6),
                    "buy_from": f"{buy_from[1].capitalize()}",
                    "sell_to": f"{sell_to[1].capitalize()}",
                    "buy_price": buy_from[2],
                    "sell_price": sell_to[2],
                    "network": buy_from[0]
                }
            else:
                print(f"⛔ Spread {spread:.6f}% inferior al mínimo (0.5%)")

        return None

    except Exception as e:
        print(f"❌ Error en scan_prices: {e}")
        return None
