from flask import Flask, jsonify, request
from binance.client import Client
from binance.enums import *
import os

app = Flask(__name__)

# Binance API Keys (use your actual keys or env vars)
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
client = Client(API_KEY, API_SECRET)

# State
strategy = "trend_following"
auto_trading_enabled = False
last_trade_price = 0
grid_levels = [100, 105, 110]  # Example grid

# --- Strategies ---
def trend_following(current_price, short_ma, long_ma):
    if short_ma > long_ma:
        return "buy"
    elif short_ma < long_ma:
        return "sell"
    return "hold"

def scalping(price, bid_price, ask_price, spread_threshold=0.001):
    spread = ask_price - bid_price
    if spread >= spread_threshold:
        if price <= bid_price:
            return "buy"
        elif price >= ask_price:
            return "sell"
    return "hold"

def grid_trading(price, grid_levels, last_price):
    for level in grid_levels:
        if price <= level and last_price > level:
            return "buy"
        elif price >= level and last_price < level:
            return "sell"
    return "hold"

# Auto strategy switch (basic logic)
def auto_switch_strategy(price, bid, ask, short_ma, long_ma):
    if abs(ask - bid) > 0.01 * price:
        return "scalping"
    elif abs(short_ma - long_ma) > 0.5:
        return "trend_following"
    else:
        return "grid_trading"

# Fetch current price and strategy
@app.route('/status')
def status():
    symbol = request.args.get('symbol', 'SOLUSDT')
    price = float(client.get_symbol_ticker(symbol=symbol)['price'])
    depth = client.get_order_book(symbol=symbol)
    bid = float(depth['bids'][0][0])
    ask = float(depth['asks'][0][0])

    # Mock MAs
    short_ma = price * 0.99
    long_ma = price * 1.01

    global strategy
    if auto_trading_enabled:
        strategy = auto_switch_strategy(price, bid, ask, short_ma, long_ma)

    return jsonify({
        "price": price,
        "strategy": strategy,
        "auto_trading": auto_trading_enabled
    })

# Toggle auto-trading
@app.route('/toggle_auto', methods=['POST'])
def toggle_auto():
    global auto_trading_enabled
    auto_trading_enabled = not auto_trading_enabled
    return jsonify({"auto_trading": auto_trading_enabled})

# Set strategy manually
@app.route('/set_strategy', methods=['POST'])
def set_strategy():
    global strategy
    strategy = request.json.get("strategy", strategy)
    return jsonify({"strategy": strategy})

if __name__ == '__main__':
    app.run(debug=True)
