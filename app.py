from flask import Flask, request
import os
from pybit.unified_trading import HTTP

app = Flask(__name__)

# Load keys
api_key = os.environ.get("BYBIT_API_KEY")
api_secret = os.environ.get("BYBIT_SECRET_KEY")

# Connect to Bybit testnet
session = HTTP(
    testnet=True,
    api_key=api_key,
    api_secret=api_secret
)

@app.route('/')
def home():
    return "Bot is running.."

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        print("Received:", data)

        action = data.get("action")

        if action == "buy":
            print("Placing BUY order")
            order = session.place_order(
                category="linear",
                symbol="BTCUSDT",
                side="Buy",
                orderType="Market",
                qty="0.001"
            )
            print(order)

        elif action == "sell":
            print("Placing SELL order")
            order = session.place_order(
                category="linear",
                symbol="BTCUSDT",
                side="Sell",
                orderType="Market",
                qty="0.001"
            )
            print(order)

    except Exception as e:
        print("Error:", e)

    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
