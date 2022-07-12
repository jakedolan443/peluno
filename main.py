import json
from flask import Flask, render_template, request


app = Flask(__name__, static_url_path='')


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

def get_config():
    with open("config.json") as f:
        user_config = json.loads(f.read())
    with open("internal.json") as f:
        internal_config = json.loads(f.read())
    return user_config | internal_config

@app.route('/coin/etc')
def Coin():
    data = []
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
    editHardStoreVariable("setup_completed", "true")
    return "OK", 200

@app.route('/')
def Index():
    data = []
    return render_template("portfolio.html", data=data)


coins = readHardStoreVariable("coin_list")









app.run(host="0.0.0.0", port=8080)


