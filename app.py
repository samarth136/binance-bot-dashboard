from flask import Flask, jsonify
from bot_runner import run_bot

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Binance Trading Bot is running!"})

@app.route('/run-bot')
def run_bot_route():
    run_bot()
    return jsonify({"message": "Bot started!"})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Use Render-assigned port or fallback to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
