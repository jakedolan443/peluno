<p align="center">
  <img style="width: 512px; height: auto;" src="https://i.imgur.com/M03U3Zw.png" />
</p>

# Peluno

Peluno is a cryptocurrency dashboard web-app to display your cryptocurrency portfolio. Includes real-time graph monitoring and prices.

This web-app is intended for self-hosting and uses the CryptoWatch Free API.

Supports over 80 cryptocurrencies and 5 fiat currencies.

# Screenshots
<img style="width: 720px;" src="https://i.imgur.com/XDsrAcm.png" />
<img style="width: 720px;" src="https://i.imgur.com/CE4V2Es.png" />

# Features
- Cryptocurrency Price Monitoring
- Historical Data Graphs
- Portfolio Management
- Support for 80+ cryptocurrencies
- Support for USD, EUR, GBP, CAD, AUD

# Installation

```
pip3 install -r requirements.txt
chmod +x peluno.py
./peluno.py
```
Peluno binds onto 0.0.0.0 port 8080.
To access the setup interface, head to http://0.0.0.0:8080

If you are using Systemd, you may use [this service file](https://gist.githubusercontent.com/jakedolan443/a4aa3cd62d7d6b5866671d13be8238ac/raw/0672392abf5eefdb35b812711df3f06deff8d2c4/peluno_systemd.service) to run peluno on boot.

# Contribute

This project does not yet have docker support - if anyone is willing, please make a pull request.

