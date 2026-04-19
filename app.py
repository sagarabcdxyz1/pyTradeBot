from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received:", data)

    action = data.get("action")

    if action == "buy":
        print("BUY signal received")
    elif action == "sell":
        print("SELL signal received")

    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
