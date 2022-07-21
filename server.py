import cryptowatch as cw
import threading
import time
import json


coins = {"ZRX":"0x",
"1INCH":"1inch",
"AAVE":"Aave",
"GHST":"Aavegotchi",
"ALGO":"Algorand",
"ANKR":"Ankr",
"ANT":"Aragon",
"REP":"Augur",
"REPV2":"Augur v2",
"AXS":"Axie Infinity",
"BADGER":"Badger DAO",
"BAL":"Balancer",
"BNT":"Bancor",
"BAND":"Band Protocol",
"BAT":"Basic Attention Token",
"BTC":"Bitcoin",
"BCH":"Bitcoin Cash",
"ADA":"Cardano",
"CTSI":"Cartesi",
"LINK":"Chainlink",
"CHZ":"Chiliz",
"COMP":"Compound",
"ATOM":"Cosmos",
"CQT":"Covalent",
"CRV":"Curve",
"DAI":"Dai",
"DASH":"Dash",
"MANA":"Decentraland",
"DOGE":"Dogecoin",
"EWT":"Energy Web Token",
"ENJ":"Enjin Coin",
"MLN":"Enzyme Finance",
"EOS":"EOS",
"ETH":"Ethereum",
"ETC":"Ethereum Classic",
"FIL":"Filecoin",
"FLOW":"Flow",
"GNO":"Gnosis",
"ICX":"ICON",
"INJ":"Injective Protocol",
"KAR":"Karuna",
"KAVA":"Kava",
"KEEP":"Keep Network",
"KSM":"Kusama",
"KNC":"Kyber Network",
"LSK":"Lisk",
"LTC":"Litecoin",
"LPT":"Livepeer",
"LRC":"Loopring",
"MKR":"Maker",
"MINA":"Mina",
"MIR":"Mirror Protocol",
"XMR":"Monero",
"MOVR":"Moonriver",
"NANO":"Nano",
"OCEAN":"Ocean",
"OMG":"OmiseGO",
"OXT":"Orchid",
"OGN":"Origin Protocol",
"PAXG":"PAX Gold",
"PERP":"Perpetual Protocol",
"DOT":"Polkadot",
"MATIC":"Polygon",
"QTUM":"Qtum",
"REN":"REN Protocol",
"RARI":"Rarible",
"XRP":"Ripple",
"SRM":"Serum",
"SC":"Siacoin",
"SOL":"Solana",
"XLM":"Stellar",
"SUSHI":"Sushi",
"SNX":"Synthetix",
"TBTC":"tBTC",
"USDT":"Tether",
"XTZ":"Tezos",
"GRT":"The Graph",
"SAND":"The Sandbox",
"TRX":"Tron",
"UNI":"Uniswap",
"USDC":"USD Coin",
"WAVES":"WAVES",
"WBTC":"Wrapped Bitcoin",
"YFI":"Yearn Finance",
"ZEC":"Zcash",
"XMR":"Monero"}
    

def get_data_for_coin(coin):
    try:
        coin = coin.lower()
        with open("data/{}_history.json".format(coin)) as f:
            existing_data = json.loads(f.read())
        data = {"coin":coin, "coin_full_name":"{} ({})".format(coins[coin.upper()], coin.upper()), "historic":[[],[]]}
        for entry in existing_data:
            data["historic"][0].append(float(entry)*1000)
            data["historic"][1].append(float(existing_data[entry]["price"]))
        data["price"] = float(data["historic"][1][-1])
        print(list(sorted(existing_data.items(), key = lambda x: x[0]))[0][0])
        data['change'] = list(sorted(existing_data.items(), key = lambda x: x[0]))[0][1]['change']
        data['change'] = list(sorted(existing_data.items(), key = lambda x: x[0]))[0][1]['change']
        print(data)
        return data
    except FileNotFoundError:
        return {"coin":coin, "coin_full_name":"{} ({})".format(coins[coin.upper()], coin.upper()), "historic":[[],[]], "price":" ?.??", "change":"", "change_colour":"green"}

def save_new_data(coin, data):
    coin = coin.lower()
    try:
        with open("data/{}_history.json".format(coin)) as f:
            existing_data = json.loads(f.read())
        existing_data[time.time()] = data
        with open("data/{}_history.json".format(coin), "w") as f:
            f.write(json.dumps(existing_data))
    except FileNotFoundError:
        data = {time.time():data}
        with open("data/{}_history.json".format(coin), "w") as f:
            f.write(json.dumps(data))

def get_exchange_rate(currency): #from USD
    if currency == "USD":
        return 1
    with open("exchange_rate.json", "r") as f:
        exchange_rate = json.loads(f.read())
    return exchange_rate["conversion_rates"][currency]

def fetch_coin_price(api_key, coin, currency):
    print("attempting to fetch for {}".format(coin))
    cw.api_key = api_key
    req = cw.markets.get("KRAKEN:{}USD".format(coin))
    candles = cw.markets.get("KRAKEN:{}USD".format(coin), ohlc=False)
    data = req._http_response._content.decode()
    d = {}
    d['price'] = "{:.2f}".format(round(get_exchange_rate(currency)*float(data.split('"last":')[1].split(",")[0]), 2))
    real_change = round(float(data.split('"change":')[1].split(",")[0].split(":")[1])*100, 2)
    if real_change > 0:
        d['change_colour'] = "green"
    else:
        d['change_colour'] = "red"
    d['change'] = "{:.2f}%".format(real_change)
    d['code'] = coin
    d['name'] = coin
    print("saved data for {}".format(coin))
    save_new_data(coin, d)

