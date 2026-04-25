from flask import Flask, request
import logging
import sys
import os
from binance.client import Client

app = Flask(__name__)

# Clean logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

print("BOT STARTED")

# 🔐 Binance TESTNET keys
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")

client = Client(API_KEY, API_SECRET)
client.API_URL = "https://testnet.binance.vision/api"

# Helper: get balance
def get_balance(asset_name):
    account = client.get_account()
    for asset in account["balances"]:
        if asset["asset"] == asset_name:
            return float(asset["free"])
    return 0.0

# Home
@app.route("/")
def home():
    return "Bot running"

# ✅ Balance endpoint
@app.route("/balance")
def balance():
    try:
        usdt = get_balance("USDT")
        btc = get_balance("BTC")
        return f"USDT: {usdt} | BTC: {btc}"
    except Exception as e:
        return str(e)

# ✅ Orders endpoint
@app.route("/orders")
def orders():
    try:
        orders = client.get_all_orders(symbol="BTCUSDT", limit=5)
        return str(orders)
    except Exception as e:
        return str(e)

# Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(silent=True)

        if not data:
            return "ok", 200

        action = data.get("action")

        before_usdt = get_balance("USDT")
        before_btc = get_balance("BTC")

        if action == "buy":
            print("BUY")
            client.order_market_buy(
                symbol="BTCUSDT",
                quantity=0.0001
            )

        elif action == "sell":
            print("SELL")
            client.order_market_sell(
                symbol="BTCUSDT",
                quantity=0.0001
            )

        else:
            print("Invalid signal")
            return "ok", 200

        after_usdt = get_balance("USDT")
        after_btc = get_balance("BTC")

        print(f"USDT: {before_usdt} -> {after_usdt}")
        print(f"BTC: {before_btc} -> {after_btc}")
        print("-----")

    except Exception as e:
        print(f"ERROR: {str(e)}")

    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
	app.run(host="0.0.0.0", port=port)
