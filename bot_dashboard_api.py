from flask import Flask, jsonify, request
from flask_cors import CORS
from binance_client import (
    get_spot_balance,
    get_price,
    set_strategy,
    get_auto_trading_status,
    toggle_auto_trading
)

app = Flask(__name__)
CORS(app)

@app.route('/balance/<symbol>', methods=['GET'])
def get_balance(symbol):
    try:
        balance = get_spot_balance(symbol)
        return jsonify({"symbol": symbol, "balance": balance})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/price/<symbol>', methods=['GET'])
def get_symbol_price(symbol):
    try:
        price = get_price(symbol)
        return jsonify({"symbol": symbol, "price": price})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/strategy', methods=['POST'])
def change_strategy():
    try:
        data = request.get_json()
        strategy = data.get("strategy")
        if not strategy:
            return jsonify({"error": "Strategy not provided"}), 400
        set_strategy(strategy)
        return jsonify({"message": "Strategy updated", "strategy": strategy})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/auto-trading/status', methods=['GET'])
def get_auto_trading():
    try:
        status = get_auto_trading_status()
        return jsonify({"auto_trading": status})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/auto-trading/toggle', methods=['POST'])
def toggle_auto():
    try:
        status = toggle_auto_trading()
        return jsonify({"message": "Auto trading status toggled", "status": status})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5050)
