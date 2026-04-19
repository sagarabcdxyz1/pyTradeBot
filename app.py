from flask import Flask, request

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