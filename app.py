from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        print("Received:", data)

        action = data.get("action")

        if action == "buy":
            print("BUY signal received")
        elif action == "sell":
            print("SELL signal received")

    except Exception as e:
        print("Error:", e)

    # 🔥 ALWAYS return fast response
    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
