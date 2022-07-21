import json
from flask import Flask, render_template, request, redirect
import server
from threading import Thread
import time
import requests


app = Flask(__name__, static_url_path='')

def update_coin_loop():
    while True:
        if not readHardStoreVariable("setup_completed") == "false":
            try:
                for coin in readPortfolio():
                    server.fetch_coin_price("{}".format(readHardStoreVariable("crypto_api_key")), coin['coin'], "{}".format(readHardStoreVariable("currency")))
            except Exception as e:
                print(str(e))
                pass
        time.sleep(1800)


def update_exchange_rate():
    if (readHardStoreVariable("currency") == "USD"):
        return
    while True:
        if not readHardStoreVariable("setup_completed") == "false":
            try:
                currency_url = 'https://v6.exchangerate-api.com/v6/{}/latest/USD'.format(readHardStoreVariable("currency_api_key"))
                response = requests.get(currency_url).json()
                with open("exchange_rate.json", "w") as f:
                    f.write(json.dumps(response))
            except Exception as e:
                print(str(e))
                pass
        time.sleep(10000)






GREEN = "#41e01f"
RED = "#ea695c"
GREY = "#b3c0be" 
currency_symbols = {"USD":"$", "EUR":"€", "GBP":"£", "AUD":"$", "CAD":"$"}


def add_new_coin(data):
    portfolio = readPortfolio()
    for coin in data['coins']:
        portfolio.append({"coin":coin, "amount":"{:.5f}".format(float(data['amount']))})
    with open("data/portfolio.json", "w") as f:
        f.write(json.dumps(portfolio))
        

def readPortfolio():
    with open("data/portfolio.json", "r") as f:
        data = json.loads(f.read())
    try:
        return data
    except KeyError:
        return

def readHardStoreVariable(var):
    with open("hard_store_vars.json", "r") as f:
        data = json.loads(f.read())
    try:
        return data[var]
    except KeyError:
        return
    
def editHardStoreVariable(var, new_data):
    with open("hard_store_vars.json", "r") as f:
        data = json.loads(f.read())
    try:
        data[var] = new_data
    except KeyError:
        return
    with open("hard_store_vars.json", "w") as f:
        data = f.write(json.dumps(data))



@app.route('/coin/<coin>')
def Coin(coin):
    data = server.get_data_for_coin(coin)
    data['currency'] = readHardStoreVariable("currency")
    data['currency_symbol'] = readHardStoreVariable("currency_symbol")
    data['mode'] = readHardStoreVariable("mode")
    data['single_price'] = data['price']
    amount = 1
    for item in readPortfolio():
        if item['coin'].lower() == coin.lower():
            amount = float(item['amount'])
            break
    for i in range(len(data['historic'][1])):
        data['historic'][1][i] = data['historic'][1][i]*amount
        
    try:
        data['price'] = "{:20,.2f}".format(float(data['price'])*amount)
    except ValueError:
        pass
    data['amount'] = amount
    return render_template("coin.html", data=data)

@app.route('/settings')
def Settings():
    data = []
    return render_template("settings.html", data=data)

@app.route('/setup', methods=["GET"])
def Setup_GET():
    data = {"coins":coins}
    return render_template("setup.html", data=data)

@app.route('/setup', methods=["POST"])
def Setup_POST():
    data = request.json
    editHardStoreVariable("crypto_api_key", data['crypto_api_key'])
    editHardStoreVariable("currency_api_key", data['currency_api_key'])
    editHardStoreVariable("mode", data['mode'])
    editHardStoreVariable("currency", data['currency'].upper())
    editHardStoreVariable("currency_symbol", currency_symbols[data['currency'].upper()])
    editHardStoreVariable("setup_completed", "true")
    markets = []
    for market in data['monitorMarkets']:
        markets.append({"coin":market, "amount":"1"})
    with open("data/portfolio.json", "w") as f:
        f.write(json.dumps(markets))
    return "OK", 200

@app.route('/')
def Index_GET():
    if readHardStoreVariable("setup_completed") == "false":
        return redirect("/setup", code=302)
    portfolio = readPortfolio()
    prices = []
    changes = []
    y = 192
    for i in range(len(portfolio)):
        portfolio[i]["coin_lowercase"] = portfolio[i]["coin"].lower()
        portfolio[i]['coord_y'] = y
        portfolio[i]["coin_full_name"] = "{} ({})".format(coins[portfolio[i]["coin"]], portfolio[i]["coin"])
        if readHardStoreVariable("mode") == "portfolio":
            portfolio[i]["command_word"] = "Owned"
        else:
            portfolio[i]["command_word"] = "Value"
            portfolio[i]["amount"] = "{:<07}".format(1)
        portfolio[i]["amount"] = "{:<07}".format(float(portfolio[i]['amount'][:7]))
        coin_info = server.get_data_for_coin(portfolio[i]['coin'])
        try:
            new_price = float(coin_info['price'])*float(portfolio[i]["amount"])
            portfolio[i]["price"] = "{:20,.2f}".format(new_price)
            prices.append(new_price)
        except ValueError as e:
            new_price = 0
            portfolio[i]["price"] = "{}".format(coin_info['price'])
        try:
            portfolio[i]["change"] = "{}%".format(abs(float(coin_info['change'].split("%")[0])))
        except ValueError:
            portfolio[i]["change"] = ""
        try:
            changes.append(new_price*(float(coin_info['change'].split("%")[0])/100))
            if changes[-1] < 0:
                portfolio[i]["change_ve"] = "-"
                portfolio[i]["change_colour"] = RED
            else:
                portfolio[i]["change_ve"] = "+"
                portfolio[i]["change_colour"] = GREEN
        except ValueError:
            portfolio[i]["change_colour"] = GREY
        y += 76
    total_change = sum(changes)
    if total_change < 0:
        total_change_ve = "-"
        total_change_colour = RED
    else:
        total_change_ve = "+"
        total_change_colour = GREEN
    data = {"coins":coins, "mode":readHardStoreVariable("mode"), "portfolio":portfolio, "currency_symbol":readHardStoreVariable("currency_symbol"), "total":"{:20,.2f}".format(sum(prices)), "total_change":"{:.2f}".format(abs(total_change)), "total_change_ve":total_change_ve, "total_change_colour":total_change_colour}
    return render_template("portfolio.html", data=data)


@app.route('/change-order', methods=["POST"])
def Change_Order_POST():
    data = request.json
    one = int((int(data['one'].split("px")[0])-192)/76)
    two = int((int(data['two'].split("px")[0])-192)/76)
    print(one, two)
    portfolio = readPortfolio()
    tmp = portfolio[two]
    portfolio[two] = portfolio[one]
    portfolio[one] = tmp
    with open("data/portfolio.json", "w") as f:
        f.write(json.dumps(portfolio))
    return "OK", 200

@app.route('/delete', methods=["POST"])
def Delete_POST():
    data = request.json
    portfolio = readPortfolio()
    new_portfolio = []
    for item in portfolio:
        if not (item['coin'].lower() == data['coin'].lower()):
            new_portfolio.append(item)
    with open("data/portfolio.json", "w") as f:
        f.write(json.dumps(new_portfolio))
    return "OK", 200

@app.route('/', methods=["POST"])
def Index_POST():
    data = request.json
    add_new_coin(data)
    return "OK", 200



coins = server.coins






Thread(target=update_exchange_rate, daemon=True).start()
Thread(target=update_coin_loop, daemon=True).start()
app.run(host="0.0.0.0", port=8080)


