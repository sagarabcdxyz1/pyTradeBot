from flask import Flask, request
import os
import logging
import sys
from pybit.unified_trading import HTTP

app = Flask(__name__)

# 🔥 Proper logging (works on all hosts)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logging.info("🚀 BOT STARTED")

# 🔐 Load API keys
api_key = os.environ.get("BYBIT_API_KEY")
api_secret = os.environ.get("BYBIT_SECRET_KEY")

logging.info(f"🔑 API KEY LOADED: {bool(api_key)}")

# 🔗 Connect to Bybit Testnet
session = HTTP(
    testnet=True,
    api_key=api_key,
    api_secret=api_secret
)

@app.route('/')
def home():
    return "Bot is running"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        logging.info("🔥 Webhook hit")

        raw_data = request.data
        logging.info(f"RAW BODY: {raw_data}")

        data = request.get_json(silent=True)
        logging.info(f"JSON: {data}")

        if not data:
            logging.info("❌ No JSON received")
            return "ok", 200

        action = data.get("action")
        logging.info(f"👉 ACTION: {action}")

        if action == "buy":
            logging.info("🚀 Placing BUY order")

            try:
                order = session.place_order(
                    category="linear",
                    symbol="BTCUSDT",
                    side="Buy",
                    orderType="Market",
                    qty="0.001"
                )
                logging.info(f"✅ ORDER RESPONSE: {order}")

            except Exception as e:
                logging.error(f"❌ ORDER ERROR (BUY): {str(e)}")

        elif action == "sell":
            logging.info("🚀 Placing SELL order")

            try:
                order = session.place_order(
                    category="linear",
                    symbol="BTCUSDT",
                    side="Sell",
                    orderType="Market",
                    qty="0.001"
                )
                logging.info(f"✅ ORDER RESPONSE: {order}")

            except Exception as e:
                logging.error(f"❌ ORDER ERROR (SELL): {str(e)}")

        else:
            logging.info("❌ Invalid action")

    except Exception as e:
        logging.error(f"❌ GENERAL ERROR: {str(e)}")

    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
